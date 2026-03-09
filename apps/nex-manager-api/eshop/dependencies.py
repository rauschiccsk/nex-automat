"""ESHOP authentication dependencies — tenant resolution by API token."""

from fastapi import Depends, Header, HTTPException, status

from database import get_db


async def get_tenant_by_token(
    x_eshop_token: str = Header(..., alias="X-Eshop-Token"),
    db=Depends(get_db),
) -> dict:
    """Resolve tenant from X-Eshop-Token header.

    Returns tenant dict or raises 401.
    """
    cur = db.cursor()
    cur.execute(
        "SELECT tenant_id, company_name, domain, brand_name, logo_url, "
        "primary_color, currency, vat_rate_default, default_lang, is_active "
        "FROM eshop_tenants WHERE api_token = %s AND is_active = TRUE",
        (x_eshop_token,),
    )
    row = cur.fetchone()
    if not row:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Neplatný alebo neaktívny eshop token",
        )
    return {
        "tenant_id": row[0],
        "company_name": row[1],
        "domain": row[2],
        "brand_name": row[3],
        "logo_url": row[4],
        "primary_color": row[5],
        "currency": row[6],
        "vat_rate_default": row[7],
        "default_lang": row[8],
        "is_active": row[9],
    }


async def get_tenant_by_mufis_key(
    api_key: str = Header(..., alias="API-KEY"),
    db=Depends(get_db),
) -> dict:
    """Resolve tenant from API-KEY header (MuFis integration).

    Returns tenant dict or raises 401.
    """
    cur = db.cursor()
    cur.execute(
        "SELECT tenant_id, company_name, domain, brand_name, logo_url, "
        "primary_color, currency, vat_rate_default, default_lang, is_active "
        "FROM eshop_tenants WHERE mufis_api_key = %s AND is_active = TRUE",
        (api_key,),
    )
    row = cur.fetchone()
    if not row:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Neplatný alebo neaktívny MuFis API kľúč",
        )
    return {
        "tenant_id": row[0],
        "company_name": row[1],
        "domain": row[2],
        "brand_name": row[3],
        "logo_url": row[4],
        "primary_color": row[5],
        "currency": row[6],
        "vat_rate_default": row[7],
        "default_lang": row[8],
        "is_active": row[9],
    }
