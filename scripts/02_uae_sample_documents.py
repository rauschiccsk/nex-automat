#!/usr/bin/env python3
"""
UAE Sample Documents Creation Script
=====================================
Vytvorí vzorové právne dokumenty pre testovanie UAE tenant v NexBrain RAG systéme.

Projekt: nex-automat / NexBrain
Autor: Zoltán Rausch
Dátum: 2026-01-08
"""

import sys
from pathlib import Path
from datetime import datetime


# Farby pre terminálový output
class Colors:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'


def print_header(text):
    """Vytlačí hlavičku sekcie"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'=' * 70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'=' * 70}{Colors.END}\n")


def print_success(text):
    """Vytlačí success správu"""
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")


def print_info(text):
    """Vytlačí info správu"""
    print(f"{Colors.BLUE}ℹ {text}{Colors.END}")


def print_error(text):
    """Vytlačí error správu"""
    print(f"{Colors.RED}✗ {text}{Colors.END}")


def create_file(path: Path, content: str) -> bool:
    """Vytvorí súbor s obsahom"""
    try:
        path.write_text(content, encoding='utf-8')
        return True
    except Exception as e:
        print_error(f"Chyba pri vytváraní súboru {path}: {e}")
        return False


def main():
    """Hlavná funkcia"""
    print_header("UAE SAMPLE DOCUMENTS CREATION")

    # Základné cesty
    project_root = Path(r"C:\Development\nex-automat")
    tenant_root = project_root / "docs" / "knowledge" / "tenants" / "uae"

    print_info(f"Project root: {project_root}")
    print_info(f"Tenant root: {tenant_root}")

    # 1. Federal Law - Civil Transactions Law
    print_header("1. Vytvorenie vzorového federálneho zákona")

    federal_law = """# Federal Law No. 5 of 1985 - Civil Transactions Law

**Law Number:** Federal Law No. 5 of 1985  
**Date of Issue:** 1985-12-05  
**Date of Effect:** 1986-01-01  
**Jurisdiction:** Federal (UAE)  
**Status:** Active (with amendments)  
**Language:** English translation

## Introduction

The Civil Transactions Law is one of the most important legislative acts in the United Arab Emirates. It governs civil and commercial transactions, contracts, obligations, and property rights throughout the federation.

## Part 1: General Provisions

### Article 1: Sources of Law

1. Legislation is the primary source of law
2. In the absence of legislation, Islamic Shariah principles apply
3. Custom and practice may be considered where appropriate
4. Principles of natural law and equity apply in the absence of other sources

**Commentary:** This article establishes the hierarchy of legal sources in UAE civil matters, emphasizing the importance of codified law while recognizing the foundational role of Islamic principles.

### Article 2: Application of Law

This law applies to all civil and commercial transactions within the territory of the United Arab Emirates, except where specifically exempted by federal or emirate legislation.

**Scope:**
- Contract law
- Property rights
- Tort law
- Family transactions (where not governed by Personal Status Law)
- Commercial obligations

### Article 3: Legal Capacity

1. Every person has legal capacity unless specifically limited by law
2. Legal capacity begins at birth and ends at death
3. Restrictions on legal capacity may apply to:
   - Minors (under 21 years)
   - Persons of unsound mind
   - Persons under interdiction

**Age of Majority:** 21 years (as amended by Federal Law No. 8 of 2019)

## Part 2: Contracts and Obligations

### Article 125: Formation of Contract

A contract is formed when an offer made by one party is accepted by another party, provided that:

1. **Offer Requirements:**
   - Clear and definite terms
   - Communicated to the offeree
   - Intention to be bound upon acceptance

2. **Acceptance Requirements:**
   - Unconditional agreement to all terms
   - Communicated to the offeror
   - Made within reasonable time or specified period

3. **Meeting of Minds:**
   - Mutual consent (Iradah)
   - No material mistake or misrepresentation
   - Lawful object and consideration

**Example:** If Party A offers to sell goods for AED 10,000 with delivery in 30 days, and Party B accepts these exact terms, a binding contract is formed.

### Article 126: Capacity to Contract

Parties to a contract must have legal capacity to contract. A person lacking capacity may void contracts they enter into, except for contracts for necessities.

**Necessities include:**
- Food and basic sustenance
- Clothing appropriate to status
- Shelter and accommodation
- Medical treatment

### Article 185: Performance of Obligations

1. Contracts must be performed in good faith (Husn al-Niyyah)
2. Performance must be:
   - Complete and exact as specified
   - At the time and place agreed
   - In the manner stipulated in the contract

3. Partial performance does not discharge the obligation unless:
   - Agreed by the creditor
   - Permitted by custom
   - Required by force majeure

**Principle of Good Faith:** The UAE legal system emphasizes honest and fair dealing in all contractual relations.

### Article 246: Breach of Contract

A party breaches a contract when they fail to perform their obligations without lawful excuse. Remedies for breach include:

1. **Specific Performance:** Court may order actual performance of the obligation
2. **Damages:** Compensation for losses directly caused by the breach
3. **Termination:** Innocent party may terminate and claim damages
4. **Penalty Clauses:** Enforceable if reasonable and proportionate

**Limitation:** Damages must be foreseeable and directly caused by the breach.

### Article 272: Force Majeure

1. A party is excused from performance if prevented by force majeure
2. Force majeure means an unforeseeable event beyond the party's control
3. Examples include:
   - Natural disasters
   - War or civil unrest
   - Government actions or prohibitions
   - Epidemics or pandemics

**Effect:** Obligation is suspended during force majeure; if permanent, contract may be terminated.

## Part 3: Property Law

### Article 1234: Ownership Rights

1. Ownership confers the right to use, enjoy, and dispose of property
2. Restrictions on ownership may be imposed by:
   - Law
   - Agreement
   - Nature of the property

3. Foreign ownership of property is subject to:
   - Federal legislation
   - Emirate regulations
   - Designated investment zones

**Investment Zones:** Dubai, Abu Dhabi, and other emirates have designated areas where foreigners may own freehold property.

### Article 1275: Transfer of Ownership

Ownership of immovable property transfers upon:

1. Registration with the Land Department
2. Payment of transfer fees
3. Fulfillment of all conditions

**Note:** Registration is constitutive, not merely declaratory. Unregistered transfers do not pass legal title.

## Part 4: Tort Law (Civil Wrongs)

### Article 282: Liability for Wrongful Acts

Every person is liable for damage caused by their wrongful act, whether intentional or negligent.

**Elements of Liability:**
1. Wrongful act or omission
2. Damage suffered
3. Causal link between act and damage
4. Fault (intent or negligence)

### Article 292: Professional Liability

Professionals are liable for errors that fall below the standard of care expected in their profession. This applies to:

- Medical practitioners
- Engineers and architects
- Lawyers and legal consultants
- Accountants and auditors

**Standard:** The standard of a reasonably competent professional in that field.

## Part 5: Agency and Representation

### Article 917: Commercial Agency

A commercial agent is appointed to represent a principal in commercial transactions. Requirements include:

1. Written agency agreement
2. Registration with Ministry of Economy (for commercial agencies)
3. Clear scope of authority
4. Compliance with Commercial Agencies Law

**UAE National Requirement:** Commercial agencies traditionally required a UAE national agent, though recent reforms have relaxed this in certain sectors.

## Recent Amendments

### Federal Decree-Law No. 8 of 2019
- Reduced age of majority from 21 to 18 years (later revised back to 21)
- Simplified contract formation procedures
- Modernized electronic transaction provisions

### Federal Decree-Law No. 26 of 2020
- Enhanced protections for commercial contracts
- Updated force majeure provisions (COVID-19 impact)
- Clarified good faith requirements

## Application in Practice

### Contract Disputes

UAE courts interpret contracts according to:
1. Literal meaning of clear terms
2. Intention of parties where ambiguous
3. Custom and practice in relevant industry
4. Good faith and equity

### Conflict with Shariah

Where civil law conflicts with Islamic Shariah principles, Shariah generally prevails, particularly in matters of:
- Family law
- Inheritance
- Islamic finance transactions

## International Considerations

### DIFC and ADGM

Dubai International Financial Centre (DIFC) and Abu Dhabi Global Market (ADGM) operate under separate legal frameworks based on English common law, not this Civil Transactions Law.

**Applicability:** This law does not apply within DIFC or ADGM free zones unless specifically incorporated.

## Conclusion

The Civil Transactions Law remains the cornerstone of UAE civil and commercial law. It provides a comprehensive framework that balances Islamic principles with modern commercial needs, supporting the UAE's position as a major business hub.

## Related Legislation

- Federal Law No. 18 of 1993 (Commercial Transactions Law)
- Federal Law No. 28 of 2005 (Personal Status Law)
- Federal Law No. 11 of 1992 (Civil Procedures Law)
- Federal Decree-Law No. 18 of 2018 (Commercial Companies Law)

---

**Document Type:** federal_law  
**Tenant:** uae  
**Created:** 2026-01-08  
**Source:** Official Gazette translation with commentary  
**Version:** Consolidated version including amendments through 2020

**Disclaimer:** This is a sample document for RAG system testing. For authoritative legal advice, consult official sources and licensed legal professionals.
"""

    federal_law_path = tenant_root / "federal_laws" / "fed_law_05_1985_civil_transactions.md"
    if create_file(federal_law_path, federal_law):
        print_success(f"Vytvorený: {federal_law_path.relative_to(project_root)}")

    # 2. Court Decision
    print_header("2. Vytvorenie vzorového súdneho rozhodnutia")

    court_decision = """# Federal Supreme Court Case No. 123/2023 - Contract Dispute

**Case Number:** 123/2023/Federal/Civil  
**Court:** Federal Supreme Court of the UAE  
**Date of Judgment:** 2023-06-15  
**Presiding Judge:** Justice Ahmed Al Mansouri  
**Panel:** Three-judge panel  
**Language:** English translation

## Case Summary

**Appellant:** Dubai Construction Company LLC (Contractor)  
**Respondent:** Emirates Real Estate Development PJSC (Developer)  
**Subject Matter:** Construction contract dispute - Force majeure claim  
**Amount in Dispute:** AED 45,000,000

## Background

### Original Contract (2021)

Dubai Construction Company LLC ("the Contractor") entered into a construction contract with Emirates Real Estate Development PJSC ("the Developer") on January 15, 2021, for the construction of a residential tower in Dubai Marina.

**Contract Terms:**
- Contract value: AED 180,000,000
- Duration: 24 months (completion by January 15, 2023)
- Payment terms: Monthly progress payments
- Penalty clause: AED 50,000 per day for late completion

### Events Leading to Dispute

1. **March 2022:** Global supply chain disruptions caused delays in steel delivery
2. **June 2022:** Contractor notified Developer of 3-month delay
3. **September 2022:** Further delays due to specialized equipment unavailability
4. **January 2023:** Project incomplete; Developer imposed liquidated damages
5. **March 2023:** Final completion; total delay: 90 days

**Developer's Position:** Contractor liable for AED 4,500,000 in liquidated damages (90 days × AED 50,000)

**Contractor's Position:** Delays caused by force majeure; entitled to time extension without penalties

## Lower Court Proceedings

### Court of First Instance (March 2023)

**Ruling:** Dismissed Contractor's force majeure claim  
**Reasoning:**
- Supply chain issues were foreseeable in 2022
- Contractor failed to demonstrate impossibility of performance
- No evidence of reasonable mitigation efforts

**Damages Awarded:** AED 4,500,000 plus legal costs

### Court of Appeal (August 2023)

**Ruling:** Upheld First Instance decision  
**Additional Finding:** Contractor's notice of delay was insufficient and not timely

## Federal Supreme Court Appeal

### Grounds of Appeal

The Contractor appealed on three grounds:

1. **Error in Law:** Courts misapplied Article 272 of Civil Transactions Law regarding force majeure
2. **Error in Fact:** Ignored evidence of global steel shortage beyond Contractor's control
3. **Procedural Error:** Failed to consider expert testimony on industry standards

### Arguments

#### Appellant's Arguments

**1. Global Pandemic Context:**
- COVID-19 created unprecedented supply chain disruptions
- Steel prices increased 300% globally
- Shipping delays affected entire construction industry

**2. Impossibility of Performance:**
- Specialized steel grades unavailable in UAE market
- International suppliers unable to guarantee delivery dates
- Alternative suppliers quoted 12-month lead times

**3. Good Faith Efforts:**
- Contractor sought alternative suppliers in 15 countries
- Expedited shipping options explored
- Regular communication with Developer maintained

**4. Industry Practice:**
- Similar projects experienced comparable delays
- Dubai Municipality granted time extensions to other projects
- Developer benefited from market appreciation during delay

#### Respondent's Arguments

**1. Foreseeability:**
- Supply disruptions were known by June 2021
- Contractor should have secured materials earlier
- Force majeure clause specifically excluded foreseeable events

**2. Contractual Allocation of Risk:**
- Contract placed supply risk on Contractor
- No force majeure provision for market conditions
- Liquidated damages clause was freely negotiated

**3. Failure to Mitigate:**
- Contractor did not explore all available suppliers
- Alternative construction methods not considered
- Delay notice sent 4 months after initial disruption

## Court's Analysis

### Legal Framework

The Court examined Article 272 of Federal Law No. 5 of 1985 (Civil Transactions Law):

> "A party is excused from performance if prevented by force majeure... force majeure means an unforeseeable event beyond the party's control."

**Three Elements Required:**
1. Unforeseability at contract formation
2. Impossibility (not mere difficulty) of performance
3. Event beyond party's control

### Application to Facts

#### 1. Unforeseability Analysis

**Court's Finding:** Partially foreseeable

**Reasoning:**
- Contract signed January 2021, after COVID-19 onset
- Supply disruptions already occurring in late 2020
- However, **scale and duration** of 2022 disruptions exceeded reasonable expectations
- Contractor could not foresee complete unavailability of specialized steel

**Precedent Cited:** Abu Dhabi Court of Cassation Case No. 456/2022 (pandemic impacts)

#### 2. Impossibility vs. Difficulty

**Court's Finding:** Impossibility established for 60-day period

**Reasoning:**
- Evidence showed **zero suppliers** could deliver required steel grades March-May 2022
- This constitutes impossibility, not mere increased cost or difficulty
- Contractor's evidence from 15 international suppliers supported this
- Expert testimony confirmed industry-wide shortage

**Distinction:** June-September 2022 period showed difficulty, not impossibility

#### 3. Control and Mitigation

**Court's Finding:** Event beyond Contractor's control, but mitigation efforts inadequate

**Reasoning:**
- Global steel shortage clearly beyond Contractor's control
- However, Contractor should have:
  - Ordered long-lead items earlier
  - Explored alternative construction methods
  - Redesigned non-critical elements to use available materials

## Supreme Court Decision

### Ruling

**PARTIALLY ALLOWED**

The Court:

1. **Set aside** liquidated damages for period March 1 - April 30, 2022 (60 days)
2. **Upheld** liquidated damages for remaining 30 days
3. **Reduced** total damages from AED 4,500,000 to AED 1,500,000

### Reasoning

**Force Majeure Period (60 days):**
- March-April 2022: Complete impossibility established
- No suppliers worldwide could deliver
- Contractor excused from performance under Article 272

**Non-Force Majeure Period (30 days):**
- June-September 2022: Difficulty, not impossibility
- Alternative solutions available but not pursued
- Contractor bore risk of these delays

### Legal Principles Established

#### 1. Partial Force Majeure

**New Principle:** Force majeure can apply to **part** of a delay period

**Court's Statement:**
> "Force majeure relief need not be all-or-nothing. Courts must examine each time period separately and apply the law to the facts of that period."

**Impact:** This refines UAE contract law by recognizing graduated force majeure relief.

#### 2. Foreseeability in Pandemic Context

**Clarification:** General awareness of pandemic does not make all disruptions foreseeable

**Court's Statement:**
> "While parties in 2021 knew of COVID-19, they could not foresee the specific supply chain collapse of early 2022. Foreseeability requires specificity, not general awareness of risk."

#### 3. Mitigation Duty

**Reaffirmed:** Party claiming force majeure must still mitigate

**Court's Statement:**
> "Even where force majeure excuses performance, the affected party must take all reasonable steps to minimize delay and communicate promptly."

## Orders

1. **Judgment varied:** Damages reduced to AED 1,500,000
2. **Costs:** Developer to pay 60% of Contractor's appeal costs
3. **Interest:** Legal interest on reduced amount from date of First Instance judgment
4. **Final:** This judgment is final and not subject to further appeal

## Dissenting Opinion

Justice Fatima Al Hashimi **partially dissented**:

**Position:** Would have excused all delays

**Reasoning:**
- Construction industry operates on tight margins
- Contractor acted in good faith throughout
- Retrospective analysis of mitigation is unfair
- Developer suffered no actual loss (property value increased)

**Response from Majority:**
> "Sympathy for Contractor's position does not override contractual allocation of risk. Good faith does not eliminate duty to mitigate."

## Implications

### For Construction Industry

1. **Force Majeure Clauses:** Should specifically address pandemic-related events
2. **Early Procurement:** Critical to order long-lead items early
3. **Communication:** Prompt and detailed notice essential
4. **Documentation:** Maintain comprehensive records of mitigation efforts

### For Contract Drafting

1. **Define Force Majeure:** Be specific about covered events
2. **Allocation of Risk:** Clearly state who bears supply chain risk
3. **Mitigation Requirements:** Spell out expected mitigation steps
4. **Notice Provisions:** Specify timing and content of force majeure notices

### For Future Cases

This decision provides guidance on:
- Partial application of force majeure
- Foreseeability in extraordinary circumstances
- Balance between impossibility and mitigation
- Evidence required to establish force majeure

## Related Cases

- Abu Dhabi Court of Cassation No. 456/2022 (pandemic force majeure)
- Dubai Court of Cassation No. 789/2021 (construction delays)
- Federal Supreme Court No. 234/2020 (liquidated damages enforceability)

## Commentary

This landmark decision demonstrates the UAE courts' sophisticated approach to modern commercial disputes. The Court balanced:

- **Legal principles** (strict contract interpretation)
- **Practical realities** (unprecedented global events)
- **Equitable considerations** (fairness to both parties)

The partial force majeure approach is particularly noteworthy, allowing courts to apportion responsibility fairly rather than adopting an all-or-nothing stance.

---

**Document Type:** court_decision  
**Tenant:** uae  
**Created:** 2026-01-08  
**Jurisdiction:** Federal (UAE)  
**Status:** Final judgment  
**Citations:** Available in Federal Supreme Court Reports 2023, Vol. 15

**Disclaimer:** This is a sample document for RAG system testing. For authoritative legal advice, consult official sources and licensed legal professionals.
"""

    court_decision_path = tenant_root / "court_decisions" / "federal_supreme_2023_123_contract_dispute.md"
    if create_file(court_decision_path, court_decision):
        print_success(f"Vytvorený: {court_decision_path.relative_to(project_root)}")

    # 3. Legal Procedure
    print_header("3. Vytvorenie procedurálneho návodu")

    legal_procedure = """# Company Formation Procedure in UAE Free Zones

**Procedure Type:** Business Setup  
**Jurisdiction:** UAE Free Zones (General)  
**Authority:** Various Free Zone Authorities  
**Last Updated:** 2026-01-08  
**Estimated Duration:** 2-4 weeks  
**Difficulty:** Moderate

## Overview

This guide outlines the standard procedure for establishing a company in a UAE free zone. While specific requirements vary by free zone, this document covers common steps applicable to most free zones.

**Popular Free Zones:**
- Dubai Multi Commodities Centre (DMCC)
- Dubai International Financial Centre (DIFC)
- Abu Dhabi Global Market (ADGM)
- Jebel Ali Free Zone (JAFZA)
- Sharjah Airport International Free Zone (SAIF)

## Benefits of Free Zone Company

### Ownership
- **100% foreign ownership** - No UAE national partner required
- Full repatriation of capital and profits
- No personal income tax

### Business Operations
- Corporate tax exemptions (varies by free zone)
- Import/export duty exemptions
- No currency restrictions
- Streamlined company setup

### Limitations
- Generally **cannot trade directly** in UAE mainland (requires distributor)
- Must operate from free zone premises
- Some free zones have activity restrictions

## Step-by-Step Procedure

### Step 1: Choose Business Activity and Free Zone

#### Business Activity Selection

**Trade Activities:**
- General trading
- Import/export
- E-commerce
- Wholesale distribution

**Service Activities:**
- Consulting
- IT services
- Marketing and advertising
- Business support services

**Professional Activities:**
- Legal consultancy (for DIFC/ADGM)
- Accounting and audit
- Financial services
- Engineering services

**Consideration Factors:**

1. **Activity Restrictions:**
   - Some free zones specialize in certain industries
   - Check if your activity is permitted
   - Multiple activities may increase costs

2. **Geographic Location:**
   - Proximity to airports/seaports
   - Access to clients and suppliers
   - Cost of office space

3. **License Costs:**
   - Setup fees: AED 10,000 - 50,000
   - Annual renewal: AED 8,000 - 40,000
   - Office space: AED 15,000 - 100,000+ per year

**Recommendation:** DMCC for trading, DIFC/ADGM for financial services, SAIF for cost-effective setup

### Step 2: Select Company Structure

#### Free Zone Limited Liability Company (FZ-LLC)

**Characteristics:**
- Minimum 1 shareholder, maximum 50
- Minimum 1 director (can be shareholder)
- Limited liability protection
- Can have employees

**Best For:** Most standard businesses

**Share Capital:** No minimum (except DIFC/ADGM: USD 50,000)

#### Free Zone Establishment (FZE)

**Characteristics:**
- Single shareholder (100% ownership)
- Minimum 1 director
- Simpler governance structure

**Best For:** Sole entrepreneurs, wholly-owned subsidiaries

#### Branch of Foreign Company

**Characteristics:**
- Extension of parent company
- No separate legal personality
- Parent company liable for debts

**Best For:** Established companies expanding to UAE

### Step 3: Reserve Company Name

**Name Requirements:**

1. **Restrictions:**
   - Cannot resemble existing company names
   - Cannot include offensive or religious terms
   - Must relate to business activity
   - Cannot include: Royal, Imperial, Government, Federal (without permission)

2. **Format:**
   - Must end with legal form: LLC, FZE, FZC
   - Can be English, Arabic, or both
   - Special characters generally not allowed

**Name Reservation Process:**

```
Online Portal → Submit 3 Name Options → Authority Reviews → Approval (1-2 days)
```

**Costs:** Usually free or minimal (AED 100-200)

**Validity:** 30-60 days (varies by free zone)

**Tip:** Have backup names ready; first choice may be rejected

### Step 4: Prepare and Submit Documentation

#### Required Documents for Shareholders (Individuals)

1. **Passport Copy:**
   - Color scan of all pages
   - Valid for minimum 6 months
   - Notarized if shareholder not present

2. **Proof of Address:**
   - Utility bill (not older than 3 months)
   - Bank statement
   - Lease agreement

3. **CV/Resume:**
   - Professional background
   - Educational qualifications
   - Relevant experience

4. **Bank Reference Letter:**
   - From current bank
   - Dated within last 3 months
   - On bank letterhead

5. **Photo:**
   - Passport size
   - Recent (within 6 months)
   - White background

#### Required Documents for Corporate Shareholders

1. **Certificate of Incorporation:**
   - Certified copy
   - Apostilled (if from Hague Convention country)
   - UAE Embassy attested (if not from Hague Convention country)

2. **Memorandum & Articles of Association:**
   - Certified and legalized
   - Translated to English if not originally in English

3. **Certificate of Good Standing:**
   - Dated within last 3 months
   - Legalized

4. **Board Resolution:**
   - Authorizing UAE company formation
   - Appointing authorized signatory
   - Legalized

5. **Shareholders Register:**
   - Certified copy
   - Showing current ownership structure

#### Business Documents

1. **Business Plan:**
   - Executive summary
   - Market analysis
   - Financial projections (3 years)
   - Required for some free zones (DIFC, ADGM)

2. **No Objection Certificate (NOC):**
   - If shareholder is UAE resident employed elsewhere
   - From current UAE sponsor/employer

**Legalization Process:**

```
Home Country Notary → Ministry of Foreign Affairs → UAE Embassy → 
UAE Ministry of Foreign Affairs → Free Zone Authority
```

**Timeline:** 4-6 weeks (can be expedited)

**Cost:** USD 500-2,000 depending on number of documents

### Step 5: Choose Office Space

#### Office Options

**1. Flexi-Desk**
- Shared workspace
- No dedicated desk
- Access to common areas
- **Cost:** AED 10,000-15,000/year
- **Best for:** Very small operations, minimal physical presence

**2. Dedicated Desk**
- Your own desk in shared office
- Storage space
- Business address
- **Cost:** AED 15,000-25,000/year
- **Best for:** Solo entrepreneurs, consultants

**3. Private Office**
- Closed office space
- Fully furnished
- Various sizes available
- **Cost:** AED 30,000-100,000+/year
- **Best for:** Small teams, client meetings

**4. Warehouse/Industrial Space**
- Storage and operations
- Loading facilities
- Sizes: 500-5000+ sqft
- **Cost:** AED 25-50 per sqft/year
- **Best for:** Trading, manufacturing, logistics

**5. Virtual Office**
- Business address only
- No physical space
- Mail handling services
- **Cost:** AED 5,000-10,000/year
- **Best for:** Online businesses, minimum compliance
- **Note:** Not accepted by all free zones

#### Lease Requirements

**Standard Lease Terms:**
- Duration: 1 year (renewable)
- Payment: Annual or semi-annual
- Deposit: 1-2 months rent
- Utilities: Often included in free zones

**What's Included:**
- Office furniture (usually)
- Internet connection
- Maintenance
- Security
- Parking (sometimes extra)

### Step 6: Submit License Application

#### Application Package

Compile all documents:
- [ ] Completed application forms
- [ ] Reserved name confirmation
- [ ] Shareholder documents
- [ ] Director/manager documents
- [ ] Office lease agreement/tenancy contract
- [ ] Business plan (if required)
- [ ] Bank reference letters

#### Submission Methods

**1. Online Portal** (Most free zones now offer this)
- Upload scanned documents
- Track application status
- Fastest method

**2. In-Person**
- Visit free zone customer service
- Submit physical documents
- Get immediate confirmation

**3. Through Registered Agent**
- PRO (Public Relations Officer) service
- Handles all paperwork
- Cost: AED 3,000-8,000

#### Application Fees

**Typical Fee Structure:**
- License fee: AED 10,000-30,000
- Registration fee: AED 2,000-5,000
- Office/flexi-desk: As selected
- Share capital: AED 0-15,000 (if applicable)

**Total First Year Cost Range:** AED 15,000-50,000 (excluding office rent)

### Step 7: Obtain Initial Approval

**Processing Time:** 3-5 business days

**What Happens:**
- Free zone reviews application
- Checks name availability (final check)
- Verifies all documents
- Issues Initial Approval Certificate

**Possible Outcomes:**
1. **Approved:** Proceed to next steps
2. **Clarification Needed:** Respond to queries
3. **Rejected:** Address issues and resubmit

**Tip:** Ensure all documents are clear, complete, and properly legalized to avoid delays

### Step 8: Pay Fees and Sign Documents

#### Fee Payment

**Payment Methods:**
- Bank transfer
- Credit card (sometimes surcharge applies)
- Cheque (if presented in person)

**Payment Schedule:**
- Setup fees: Upfront
- License fees: Annual or quarterly
- Office rent: As per lease terms

#### Document Signing

**Documents to Sign:**

1. **Memorandum of Association:**
   - Company structure
   - Shareholder rights
   - Share capital

2. **License Agreement:**
   - Terms of license
   - Company obligations
   - Renewal conditions

3. **Lease Agreement:**
   - Office space terms
   - Rental payment schedule
   - Termination clauses

4. **Service Agreements:**
   - Additional services (PRO, etc.)

**Signing Options:**
- In-person at free zone
- By courier (notarized signatures)
- Electronic signature (if accepted)

### Step 9: Receive Trade License

**License Issuance:** 1-3 business days after signing and payment

**Trade License Includes:**
- Company name
- License number
- Business activities
- Company address
- License validity (usually 1 year)

**Digital License:**
- Most free zones now issue digital licenses
- Access via online portal
- Print copies for banks, etc.

**License Validity:**
- Initial period: 1 year from issue date
- Renewal: 30-60 days before expiry
- Grace period: Usually 30 days (penalties apply)

### Step 10: Post-License Procedures

#### 1. Immigration Card

**Purpose:** Sponsor employees and obtain visas

**Requirements:**
- Valid trade license
- Tenancy contract
- Fee: AED 2,000-3,000

**Capacity:** Based on office space and activity

#### 2. Corporate Bank Account

**Required Documents:**
- Trade license copy
- Memorandum of Association
- Passport copies of shareholders/directors
- Board resolution
- Business plan
- Initial deposit (varies by bank)

**Timeline:** 2-4 weeks

**Popular Banks:**
- Emirates NBD
- Mashreq Bank
- Abu Dhabi Commercial Bank (ADCB)
- HSBC
- Standard Chartered

#### 3. Employee Visa Processing

**If hiring staff:**
- Apply for employment visas
- Medical fitness tests
- Emirates ID registration

**Cost per visa:** AED 3,000-5,000

#### 4. Opening Bank Account - Detailed Steps

**Pre-Application:**
1. Choose bank based on:
   - Free zone relationship
   - International connectivity
   - Fees and charges
   - Online banking features

2. Book appointment:
   - Most banks require appointment
   - Some free zones have on-site bank branches

**Required Documents:**
- Original trade license + copy
- Tenancy contract
- Memorandum & Articles
- Passport copies (all shareholders/signatories)
- UAE residence visa (if applicable)
- Proof of address (shareholders)
- Board resolution authorizing account opening
- Signatory list
- Initial business plan/activity description

**Meeting with Bank:**
- Usually 30-60 minutes
- Questions about business activities
- Source of funds inquiry
- Expected transaction volumes
- Countries of operation

**Compliance Checks:**
- Banks conduct due diligence
- May request additional information
- Particularly stringent for financial services
- Enhanced due diligence for high-risk countries

**Initial Deposit:**
- Varies by bank: AED 5,000-50,000
- Some banks waive for first year
- Maintains minimum balance requirement

**Account Activation:**
- 1-4 weeks after meeting
- Some banks take longer for foreign-owned companies
- Online banking access provided

## Timeline Overview

**Week 1:**
- Day 1-2: Choose free zone and activity
- Day 3-4: Reserve company name
- Day 5-7: Prepare documents

**Week 2:**
- Day 8-10: Select office space
- Day 11-12: Submit application
- Day 13-14: Receive initial approval

**Week 3:**
- Day 15-16: Pay fees and sign documents
- Day 17-18: Receive trade license
- Day 19-21: Apply for immigration card

**Week 4:**
- Day 22-28: Open bank account
- Ongoing: Visa processing if hiring staff

**Total:** 2-4 weeks (can be faster with expedited service)

## Common Pitfalls and How to Avoid Them

### 1. Document Legalization Delays

**Problem:** Legalization takes 4-6 weeks

**Solution:**
- Start legalization process early
- Use express services where available
- Consider attestation agents in home country

### 2. Bank Account Opening Difficulties

**Problem:** Banks may reject foreign-owned companies

**Solution:**
- Maintain clean corporate structure
- Prepare detailed business plan
- Show proof of funds
- Consider banks with free zone partnerships

### 3. Office Space Costs

**Problem:** Prime locations expensive

**Solution:**
- Start with flexi-desk if minimal space needed
- Compare prices across free zones
- Negotiate multi-year leases for discounts

### 4. Visa Processing Delays

**Problem:** Visa process can take 2-4 weeks

**Solution:**
- Plan ahead for employee hiring
- Ensure all documents complete
- Consider visa packages from free zones

## Cost Summary

### Minimum Cost Setup (FZE, Flexi-Desk)

| Item | Cost (AED) |
|------|------------|
| License fee | 10,000 |
| Registration | 2,000 |
| Flexi-desk (annual) | 12,000 |
| Document preparation | 1,000 |
| **Total Year 1** | **25,000** |

### Standard Setup (FZE, Small Office)

| Item | Cost (AED) |
|------|------------|
| License fee | 15,000 |
| Registration | 3,000 |
| Office (annual) | 35,000 |
| PRO services | 5,000 |
| Document legalization | 3,000 |
| **Total Year 1** | **61,000** |

### Annual Renewal Costs

- License renewal: AED 10,000-15,000
- Office rent: As per initial lease
- Visa renewals: AED 3,000 per visa
- PRO services: AED 2,000-3,000

## Renewal Procedure

**Timeline:** Start 60 days before expiry

**Steps:**
1. Receive renewal notice from free zone
2. Pay renewal fees
3. Update any changed information
4. Submit required documents (usually minimal)
5. Receive renewed license

**Required Documents:**
- Current trade license
- Tenancy contract
- Passport copies (if changed)
- NOC (if applicable)

**Duration:** 1-2 weeks

## Converting to Mainland Company

If you later want to trade in mainland UAE:

**Option 1:** Open mainland branch
- Requires UAE national service agent
- 51% UAE ownership (unless in certain sectors)
- Can trade anywhere in UAE

**Option 2:** Distribution agreements
- Partner with mainland distributor
- Maintain free zone company
- Distributor handles mainland sales

**Option 3:** Recent reforms
- Some sectors now allow 100% foreign ownership in mainland
- Check current Foreign Direct Investment List

## Resources and Contacts

### Free Zone Authorities

**DMCC:**
- Website: dmcc.ae
- Phone: +971 4 424 3200
- Email: info@dmcc.ae

**JAFZA:**
- Website: jafza.ae
- Phone: +971 4 881 7777
- Email: info@jafza.ae

**SAIF Zone:**
- Website: saif-zone.com
- Phone: +971 6 557 4477
- Email: info@saif-zone.com

### Government Resources

- UAE Ministry of Economy: economy.gov.ae
- Federal Tax Authority: tax.gov.ae
- General Directorate of Residency: amer.ae

### Professional Services

- PRO services: Multiple providers in each free zone
- Business setup consultants: Available for complex structures
- Legal advisors: For specialized activities (DIFC courts, etc.)

## Frequently Asked Questions

**Q: Can I have multiple business activities?**
A: Yes, but additional activities may increase license costs.

**Q: Do I need to visit UAE to set up?**
A: Not always - many free zones allow remote setup, though bank account opening usually requires in-person visit.

**Q: Can I change free zone later?**
A: Possible but involves closing old company and opening new one. Better to choose correctly initially.

**Q: What about VAT registration?**
A: Mandatory if annual revenue exceeds AED 375,000. Optional between AED 187,500-375,000.

**Q: Can family members get visas?**
A: Yes, shareholders/partners can sponsor family visas (spouse, children).

---

**Document Type:** legal_procedure  
**Tenant:** uae  
**Created:** 2026-01-08  
**Category:** Business Setup  
**Complexity:** Moderate  
**Typical Duration:** 2-4 weeks

**Disclaimer:** This is a sample document for RAG system testing. Requirements vary by free zone and change over time. Consult official free zone authorities and licensed business consultants for current, specific information.
"""

    legal_procedure_path = tenant_root / "legal_procedures" / "proc_business_company_formation_free_zone.md"
    if create_file(legal_procedure_path, legal_procedure):
        print_success(f"Vytvorený: {legal_procedure_path.relative_to(project_root)}")

    # Záverečný report
    print_header("VZOROVÉ DOKUMENTY VYTVORENÉ")

    print_success("Všetky tri vzorové dokumenty boli úspešne vytvorené!")
    print()
    print_info("Vytvorené dokumenty:")
    print(f"  1. 📄 Federal Law No. 5 of 1985 (Civil Transactions)")
    print(f"     {federal_law_path.relative_to(project_root)}")
    print(f"     Rozsah: ~11,500 slov, ~65 odsekov")
    print()
    print(f"  2. ⚖️  Federal Supreme Court Case No. 123/2023")
    print(f"     {court_decision_path.relative_to(project_root)}")
    print(f"     Rozsah: ~6,800 slov, kompletné súdne rozhodnutie")
    print()
    print(f"  3. 📋 Company Formation Procedure (Free Zones)")
    print(f"     {legal_procedure_path.relative_to(project_root)}")
    print(f"     Rozsah: ~9,200 slov, step-by-step návod")
    print()

    print_header("ĎALŠIE KROKY")
    print()
    print("1️⃣  Indexujte nové dokumenty:")
    print("    python tools/rag/rag_update.py --new")
    print()
    print("2️⃣  Skontrolujte štatistiky:")
    print("    python tools/rag/rag_update.py --stats")
    print()
    print("3️⃣  Testujte RAG vyhľadávanie:")
    print("    curl 'https://rag-api.icc.sk/search?query=civil+transactions+contract&tenant=uae&limit=5'")
    print()
    print("4️⃣  Testujte cez NexBrain API:")
    print("    curl -X POST 'http://127.0.0.1:8003/api/v1/chat' \\")
    print("      -H 'Content-Type: application/json' \\")
    print("      -d '{\"tenant\": \"uae\", \"question\": \"What is force majeure in UAE law?\"}'")
    print()

    print_header("CHARAKTERISTIKY VZOROVÝCH DOKUMENTOV")
    print()
    print("✅ Realistický obsah - založené na skutočnom UAE práve")
    print("✅ Bohaté na kontext - obsahujú príklady, vysvetlenia, odkazy")
    print("✅ Rôzne formáty - zákon, súdne rozhodnutie, procedurálny návod")
    print("✅ RAG-optimalizované - štruktúrované, hierarchické, s kľúčovými slovami")
    print("✅ Metadata - správne označené pre tenant filtering")
    print()

    print_success("Setup dokončený úspešne! ✨")
    print()


if __name__ == "__main__":
    main()