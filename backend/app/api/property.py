from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.property import PropertyRecord, PropertyAnalysisRequest, PropertyAnalysisResponse
from app.models.property import Property
from app.core.database import get_db
from app.utils.property_analysis import PropertyAnalyzer
from app.utils.ai_investment_analysis import ai_investment_analysis
from typing import List

router = APIRouter(prefix="/properties", tags=["Properties"])

@router.get("/", response_model=List[PropertyRecord])
def read_properties(db: Session = Depends(get_db)):
    properties = db.query(Property).all()
    return [PropertyRecord.from_orm(p) for p in properties]

@router.get("/{property_id}", response_model=PropertyRecord)
def read_property(property_id: int, db: Session = Depends(get_db)):
    p = db.query(Property).filter(Property.id == property_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Property not found")
    return PropertyRecord.from_orm(p)

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
        # Search by formatted_address (ORM field) rather than legacy 'address'
        property_obj = db.query(Property).filter(
            Property.formatted_address.ilike(f"%{request.address}%")
        ).first()

        if not property_obj:
            raise HTTPException(
                status_code=404,
                detail=f"Property not found for address: {request.address}"
            )

       
        property_record = PropertyRecord.from_orm(property_obj)

        # Run financial analysis
        analyzer = PropertyAnalyzer()
        financial_analysis = analyzer.analyze_property(
            property_data=property_record.dict(by_alias=True),
            calculation_mode=request.calculation_mode,
            custom_expenses=request.custom_expenses,
            cap_rate_threshold=request.cap_rate_threshold
        )

        # Generate AI insights
        cap_rate = financial_analysis.get("cap_rates", {}).get("mid", 0)
        roi = cap_rate  # Using cap rate as ROI proxy

        ai_analysis = ai_investment_analysis(
            property_data=property_record.dict(by_alias=True),
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
            address=property_obj.formatted_address,
            calculation_mode=calculation_mode,
            cap_rate_threshold=cap_rate_threshold
        )

        return await analyze_property_investment(request, db)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )
    

    #RUN CHAT WITH SWAGGERDOCS PUSH AND POST REQS 