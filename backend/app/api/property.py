from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.property_schemas import PropertyRecord, PropertyAnalysisRequest, PropertyAnalysisResponse
from app.models.property import Property
from app.core.database import get_db
from app.services.property_analysis import PropertyAnalyzer
from app.services.ai_investment_analysis import ai_investment_analysis
from typing import List

router = APIRouter(prefix="/properties", tags=["Properties"])

@router.get("/", response_model=List[PropertyRecord])
def read_properties(db: Session = Depends(get_db)):
    properties = db.query(Property).all()
    return [PropertyRecord(
        id=str(p.id),
        formattedAddress=p.address,
        addressLine1=p.address,
        city=p.city,
        state=p.state,
        zipCode=p.zip_code,
        bedrooms=p.bedrooms,
        bathrooms=p.bathrooms,
        squareFootage=p.square_feet,
        yearBuilt=p.year_built,
        lastSalePrice=p.price
    ) for p in properties]

@router.get("/{property_id}", response_model=PropertyRecord)
def read_property(property_id: int, db: Session = Depends(get_db)):
    p = db.query(Property).filter(Property.id == property_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Property not found")
    return PropertyRecord(
        id=str(p.id),
        formattedAddress=p.address,
        addressLine1=p.address,
        city=p.city,
        state=p.state,
        zipCode=p.zip_code,
        bedrooms=p.bedrooms,
        bathrooms=p.bathrooms,
        squareFootage=p.square_feet,
        yearBuilt=p.year_built,
        lastSalePrice=p.price
    )

@router.post("/analyze-property", response_model=PropertyAnalysisResponse)
async def analyze_property_investment(
    request: PropertyAnalysisRequest,
    db: Session = Depends(get_db)
):
    """
    Protected endpoint to analyze a property's investment potential.
    """
    try:
        # Find property in database by address
        property_obj = db.query(Property).filter(
            Property.address.ilike(f"%{request.address}%")
        ).first()

        if not property_obj:
            raise HTTPException(
                status_code=404,
                detail=f"Property not found for address: {request.address}"
            )

        # Convert to PropertyRecord format
        property_record = PropertyRecord(
            id=str(property_obj.id),
            formattedAddress=property_obj.address,
            addressLine1=property_obj.address,
            city=property_obj.city,
            state=property_obj.state,
            zipCode=property_obj.zip_code,
            bedrooms=property_obj.bedrooms,
            bathrooms=property_obj.bathrooms,
            squareFootage=property_obj.square_feet,
            yearBuilt=property_obj.year_built,
            lastSalePrice=property_obj.price
        )

        # Run financial analysis
        analyzer = PropertyAnalyzer()
        financial_analysis = analyzer.analyze_property(
            property_data=property_record.dict(),
            calculation_mode=request.calculation_mode,
            custom_expenses=request.custom_expenses,
            cap_rate_threshold=request.cap_rate_threshold
        )

        # Generate AI insights
        cap_rate = financial_analysis.get("cap_rates", {}).get("mid", 0)
        roi = cap_rate  # Using cap rate as ROI proxy

        ai_analysis = ai_investment_analysis(
            property_data=property_record.dict(),
            roi=roi,
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

@router.get("/analyze-property/{property_id}")
async def analyze_property_by_id(
    property_id: int,
    calculation_mode: str = "gross",
    cap_rate_threshold: float = 8.0,
    db: Session = Depends(get_db)
):
    """
    Alternative endpoint to analyze property by ID instead of address
    """
    try:
        property_obj = db.query(Property).filter(Property.id == property_id).first()

        if not property_obj:
            raise HTTPException(status_code=404, detail="Property not found")

        request = PropertyAnalysisRequest(
            address=property_obj.address,
            calculation_mode=calculation_mode,
            cap_rate_threshold=cap_rate_threshold
        )

        return await analyze_property_investment(request, db)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )