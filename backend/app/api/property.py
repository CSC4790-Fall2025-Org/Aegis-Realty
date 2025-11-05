from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core import get_db
from app.schemas.property import PropertyBase, PropertyCreate, PropertyUpdate, PropertyAnalysisRequest, \
    PropertyAnalysisResponse
from app.crud.property import (
    get_all_properties,
    get_property_by_id,
    create_property,
    update_property,
    delete_property
)
from app.utils.property_analysis import PropertyAnalyzer
from app.utils.ai_investment_analysis import ai_investment_analysis

router = APIRouter(prefix="/properties", tags=["Properties"])

@router.get("/", response_model=List[PropertyBase])
def get_properties(
        skip: int = 0,
        limit: int = 25,
        city: Optional[str] = None,
        state: Optional[str] = None,
        property_type: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        bedrooms: Optional[int] = None,
        db: Session = Depends(get_db)
):
    properties = get_all_properties(
        db=db, skip=skip, limit=limit, city=city, state=state,
        property_type=property_type, min_price=min_price,
        max_price=max_price, bedrooms=bedrooms
    )
    return [PropertyBase.model_validate(p) for p in properties]


@router.get("/{property_id}", response_model=PropertyBase)
def get_property(property_id: int, db: Session = Depends(get_db)):
    property_obj = get_property_by_id(db, property_id)
    if not property_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found"
        )
    return PropertyBase.model_validate(property_obj)


@router.post("/", response_model=PropertyBase, status_code=status.HTTP_201_CREATED)
def create_new_property(property_data: PropertyCreate, db: Session = Depends(get_db)):
    new_property = create_property(db, property_data)
    return PropertyBase.model_validate(new_property)


@router.patch("/{property_id}", response_model=PropertyBase)
def update_existing_property(
        property_id: int,
        property_data: PropertyUpdate,
        db: Session = Depends(get_db)
):
    updated_property = update_property(db, property_id, property_data)
    if not updated_property:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found"
        )
    return PropertyBase.model_validate(updated_property)


@router.delete("/{property_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_property(property_id: int, db: Session = Depends(get_db)):
    success = delete_property(db, property_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found"
        )


@router.post("/{property_id}/analysis", response_model=PropertyAnalysisResponse)
def analyze_property_investment(
        property_id: int,
        analysis_request: PropertyAnalysisRequest,
        db: Session = Depends(get_db)
):
    property_obj = get_property_by_id(db, property_id)
    if not property_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found"
        )

    analyzer = PropertyAnalyzer()
    property_dict = PropertyBase.model_validate(property_obj).model_dump()

    financial_analysis = analyzer.analyze_property(
        property_dict,
        analysis_request.calculation_mode,
        analysis_request.custom_expenses,
        analysis_request.cap_rate_threshold
    )

    ai_analysis = ai_investment_analysis(
        property_dict,
        financial_analysis["cap_rates"]["mid"]
    )

    return PropertyAnalysisResponse(
        property_data=PropertyBase.model_validate(property_obj),
        financial_analysis=financial_analysis,
        ai_analysis=ai_analysis,
        success=True,
        message="Analysis completed successfully"
    )