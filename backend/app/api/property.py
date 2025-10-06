from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.property import PropertyBase, PropertyAnalysisRequest, PropertyAnalysisResponse, PropertyCreate, PropertyUpdate
from app.models.property import Property
from app.core.database import get_db
from app.crud.property import (
    get_property_by_id,
    get_all_properties,
    create_property,
    update_property,
    delete_property
)
from app.utils.property_analysis import PropertyAnalyzer
from app.utils.ai_investment_analysis import ai_investment_analysis
from typing import List, Optional

router = APIRouter(prefix="/properties", tags=["Properties"])

@router.get("/", response_model=List[PropertyBase])
def get_properties(
    skip: int = 0,
    limit: int = 100,
    city: Optional[str] = None,
    state: Optional[str] = None,
    property_type: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    bedrooms: Optional[int] = None,
    db: Session = Depends(get_db)
):
    properties = get_properties_filtered(
        db=db,
        skip=skip,
        limit=limit,
        city=city,
        state=state,
        property_type=property_type,
        min_price=min_price,
        max_price=max_price,
        bedrooms=bedrooms
    )
    return [PropertyBase.from_orm(p) for p in properties]

@router.get("/{property_id}", response_model=PropertyBase)
def get_property(property_id: int, db: Session = Depends(get_db)):
    property_obj = get_property_by_id(db, property_id)
    if not property_obj:
        raise HTTPException(status_code=404, detail="Property not found")
    return PropertyBase.from_orm(property_obj)

@router.post("/", response_model=PropertyBase, status_code=status.HTTP_201_CREATED)
def create_new_property(
    property_data: PropertyCreate,
    db: Session = Depends(get_db)
):
    """Create a new property"""
    try:
        new_property = create_property(db, property_data)
        return PropertyBase.from_orm(new_property)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create property: {str(e)}"
        )

@router.patch("/{property_id}", response_model=PropertyBase)
def update_property_data(
    property_id: int,
    property_update: PropertyUpdate,
    db: Session = Depends(get_db)
):
    updated_property = update_property(db, property_id, property_update)
    if not updated_property:
        raise HTTPException(status_code=404, detail="Property not found")
    return PropertyBase.from_orm(updated_property)

@router.delete("/{property_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_property_by_id(
    property_id: int,
    db: Session = Depends(get_db)
):
    success = delete_property(db, property_id)
    if not success:
        raise HTTPException(status_code=404, detail="Property not found")

@router.post("/{property_id}/analysis", response_model=PropertyAnalysisResponse)
async def create_property_analysis(
    property_id: int,
    request: PropertyAnalysisRequest,
    db: Session = Depends(get_db)
):
    try:
        property_obj = get_property_by_id(db, property_id)
        if not property_obj:
            raise HTTPException(status_code=404, detail="Property not found")

        property_record = PropertyBase.from_orm(property_obj)

        analyzer = PropertyAnalyzer()
        financial_analysis = analyzer.analyze_property(
            property_data=property_record.dict(by_alias=True),
            calculation_mode=request.calculation_mode,
            custom_expenses=request.custom_expenses,
            cap_rate_threshold=request.cap_rate_threshold
        )
        cap_rate = financial_analysis.get("cap_rates", {}).get("mid", 0)

        ai_analysis = ai_investment_analysis(
            property_data=property_record.dict(by_alias=True),
            cap_rate=cap_rate
        )

        return PropertyAnalysisResponse(
            property_data=property_record,
            financial_analysis=financial_analysis,
            ai_analysis=ai_analysis,
            success=True,
            message="Property analysis completed successfully"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )