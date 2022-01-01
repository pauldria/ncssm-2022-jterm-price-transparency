# 2022 NCSSM J-Term Project: Hospital Price Transparency

## Intro

Health care in America has a lot of areas in which it can improve. A great summary is found in [this summary from the Commonwealth Fund](https://www.commonwealthfund.org/publications/issue-briefs/2020/jan/us-health-care-global-perspective-2019) comparing US health care to the rest of the world. The title ***Higher Spending, Worse Outcomes?*** summarizes the situation well. 

A fundamental problem here is that the health care system in America is a large complex of different entities:

* **Members** are people like you and I that are the ones receiving health care. 
* **Providers** are the doctors, nurses, specialists, and facilities that are utilized to provide health care.
* **Employers** or Governments (also known as Plan Sponsors) are the ones that offer health insurance to groups of people - the employees for an employer, and elderly people through Medicare for the Government (as examples). 
* **Insurers** (also known as Payers) are the primary entities that pay Providers, and they negotiate rates for these services. There are two primary different ways that a Member works with an Insurer:
  * The member could obtain insurance directly through an Insurer, where health care is provided in exchange for a recurring **premium** charge that is paid regardless of how much health care is obtained, along with additional **copay** or **coinsurance** charges every time health care is obtained. In this situation, *the Insurer is the one taking the risk*. 
  * The member could obtain insurance through an Employer or through the Government. There are similar charges involved, but the main notable difference is that *the Employer (or Government) is taking the risk*. 
  
There are no natural mechanisms in the US health care system to contain costs, and all parties involved have a motivating interest to keep costs high. 

One way in which we see this play out is through pricing obfuscation. This takes on a few different forms:
1. When a patient sees a provider, rarely do they know exactly what they are going to be getting in terms of charges and services.
2. Payers and providers don't work well together to ensure that all care provided - particularly at hospitals - is covered. Work may be performed by providers not affiliated with the hospital and charged and handled separately. 

This project won't solve the US health care problem. However, transparency is the road to better, long-term, sustainable solutions. By providing transparency in how this slice of the health care industry operates, we can start to educate and inform North Carolinians and policy makers about the real costs of maintaining the status quo. 

## Background

### CMS Price Transparency Rule

On January 1, 2021, the [CMS Hospital Price Transparency Rule](https://www.cms.gov/hospital-price-transparency/hospitals) went into effect, obliging hospitals to provide ***standard charges*** via a ***machine-readable file***. There's a lot to unpack here, but the [Resources Page](https://www.cms.gov/hospital-price-transparency/resources) has tons of information. Specifically, [this presentation](https://www.cms.gov/files/document/august-11-2021-hospital-price-transparency-odf-slide-presentation.pdf) is a great summary with these important notes:
1. **Hospitals must provide five different prices for each line item**. These are:
    - Gross charge - the "sticker price" so to speak. 
    - Discounted cash price - how much one would actually pay, if paying by cash. 
    - Payer-specific negotiated charge - this is for each Payer (insurer), and represents the cost negotiated for that item through that Payer. This only needs to be broken-out for Payers of a certain size.
    - De-identified minimum charge - over *all* Payers, what's the minimum? 
    - De-identified maximum charge - over *all* Payers, what's the maximum? 
2. **Hospitals must use common billing/accounting codes** - there's a handful of them but the main ones are [Current Procedural Terminology (CPT)](https://www.aapc.com/codes/cpt-codes-range/) codes for procedures, [Healthcare Common Procedure Coding System (HCPCS)](https://www.nlm.nih.gov/research/umls/sourcereleasedocs/current/HCPCS/index.html#:~:text=HCPCS%20is%20a%20collection%20of,by%20Medicare%20and%20other%20insurers.&text=HCPCS%20is%20divided%20into%20two%20subsystems%2C%20Level%20I%20and%20Level%20II.) codes for procedures, supplies, and services, and [Diagnosis Related Groups (DRGs)](https://www.cms.gov/Medicare/Medicare-Fee-for-Service-Payment/AcuteInpatientPPS/MS-DRG-Classifications-and-Software) for "bundles" of services that cover a common condition/issue . 
3. **Hospitals must abide by standards on their files** - it must be a machine-readable format (CMS suggests XML, JSON, and CSV but is not prescriptive here) and there is a specific naming convention of the file, which is `<EIN>_<Hospital Name>_standardcharges.<SUFFIX>`. 
4. **Data must be updated annually** - we won't be able to address this as we've only started tracking. 

### News Articles Worth Reading

The Wall Street Journal in particular has had a handful of high-profile articles about price transparency. 

* [Methodology: How the WSJ Analyzed Hospital Pricing Data](https://www.wsj.com/articles/methodology-how-the-wsj-analyzed-hospital-pricing-data-11625583571?st=xjyjpqbsvgap4q0&reflink=desktopwebshare_permalink)
* [How to Find the Cost of Hospital Medical Procedures](https://www.wsj.com/articles/how-to-find-the-cost-of-hospital-medical-procedures-11613048778?st=c1fz7rbakaq2hhu&reflink=desktopwebshare_permalink)
* [Hospitals Draw Warning on Price Disclosure Rule Compliance](https://www.wsj.com/articles/hospitals-draw-warning-on-price-disclosure-rule-compliance-11620442193?st=d263pdegi8jnb80&reflink=desktopwebshare_permalink)
* [Some Hospitals Charge Up to 10 Times More for Medical Scans Than Others, Study Finds](https://www.wsj.com/articles/some-hospitals-charge-up-to-10-times-more-for-medical-scans-than-others-study-finds-11638284400?st=v43nwyx80mnzu26&reflink=desktopwebshare_permalink)
* [Hospital Prices Are Arbitrary. Just Look at the Kingsburys’ $100,000 Bill](https://www.wsj.com/articles/hospital-prices-arbitrary-healthcare-medical-bills-insurance-11635428943?st=jicpr3yac3oj4ue&reflink=desktopwebshare_permalink)
* [Covid-19 Charges at Hospitals Can Vary by Tens of Thousands of Dollars, a WSJ Analysis Finds](https://www.wsj.com/articles/covid-19-charges-at-hospitals-can-vary-by-tens-of-thousands-of-dollars-a-wsj-analysis-finds-11633262403?st=vb5lhf3vqgkg7vl&reflink=desktopwebshare_permalink)
* [Hospitals Often Charge Uninsured People the Highest Prices, New Data Show](https://www.wsj.com/articles/hospitals-often-charge-uninsured-people-the-highest-prices-new-data-show-11625584448?st=61bgbzoc0ce8b54&reflink=desktopwebshare_permalink)

## Data

### Dataset Option 1 - Turquoise Health

[Turquoise Health](https://turquoise.health/researchers) provides a dataset for research use that is obtained in ways similar to what we're doing now. They did all the heavy lifting, but we only have an access to a slice of what's available.

This data is in BigQuery in the `INSERT DATASET HERE` dataset.

### Dataset Option 2 - NC Hospitals

Most of the fun work is diving into the data but here's how we're bringing it together. It's very similar in style to what the [Johns Hopkins COVID Data Repository](https://github.com/CSSEGISandData/COVID-19) is doing. 

1. **Find out where the data is** - each hospital has its own place where it keeps its data, and it's not consistent. [For now we're tracking those locations here](https://docs.google.com/spreadsheets/d/1xIlR14mWOBVMz0Yv9mtGC2W0_MicVOqiIiWa7UrB8b0/edit?usp=sharing) and [you first need to know what hospitals exist in NC](https://info.ncdhhs.gov/dhsr/reports.htm) and then start searching. 
2. **Munge it all into a common format** - each hospital has its own naming schema and standard, and to be effective overall we have to bring it together to a common form. We propose a data schema that is [long and tall]:

| Column | Description | 
|--------|-------------|
| `date_obtained` | Represents the date in which this table entered this dataset. |
| `date_provided` | Represents the date in which the hospital provided this data, per the hospital, if available. |
| `hospital_name` | Name of hospital. |
| `code` | Code that is utilized to describe the entry. |
| `code_type` | Classification system used for `code`. |
| `description` | Description - as provided by the hospital. |
| `standard_description` | Description - as provided by the coding association. |
| `payer` | This is the name of the Payer used, which also includes the scenarios where it's the gross charge (`_GROSS`), the minimum charge (`_MINIMUM_INPATIENT` or `_MINIMUM_OUTPATIENT`), or the maximum charge (`_MAXIMUM_INPATIENT` or `_MAXIMUM_OUTPATIENT`). |
| `plan` | This is the name of the plan utilized within this Payer. |
| `cost` | The cost. |

## Potential Questions

1. **How much of the data can you actually understand?** Put yourself in the perspective of the patient .If you looked at one of these line items in a hospital's dataset, can you infer what's actually happening and why? This is the crux of price transparency - it's not sufficient to post prices, it's necessary to provide transparency into what you are getting when you provide services to patients.
2. **How compliant are hospitals in posting prices?** There are [specific rules around 70 "shoppable services"](https://www.cms.gov/files/document/steps-making-public-standard-charges-shoppable-services.pdf) that hospitals must post, _if they provide it_. First, see what hospitals provide what from the data. Then, how do you know if the missing data is because the hospital actually does not provide, or if it's because they didn't publish the data? 🤔
3. **How awful are hospitals in terms of their price differentials, or insurers in their ability to advocate for their customers?** This occurs in a few ways:
  * Gross price versus cash price - if their gross price is way higher than one would pay at the most basic level - cash - why?
  * Max insured price versus cash price - if there are situations where it's _cheaper_ to pay cash than through insurance - why?
  * Max insured price versus min insured price - if this differential is huge - why? 

## Getting Started

There are two main things that you are being set up with: access to this data via [Google's BigQuery data platform] and a way to explore and visualize via [Mode Analytics]. You are free to use other things and explore, but it might be near-impossible to deal with the raw data outside of BigQuery although there are plenty of visualization options out there. 

### Access

You have two ways of accessing these resources:
* **Pre-made "burner" accounts** - the accounts `ncssmpricetransparency.*@gmail.com` - where `*` is either 1, 2, 3, 4, or 5 - have access. [Contact me](mailto:paul@myraff.com) for the password. 
* **Your own account** - [contact me](mailto:paul@myraff.com) with your Google account and I will give you access ASAP. 

### Quickstart: Big Query

* [This link](https://console.cloud.google.com/bigquery?project=ncssm-price-transparency) should take you directly to the Google BigQuery web console to explore and query the data, assuming you are already logged in as someone who has access.
* Data in BigQuery is organized hierarchically via **projects, datasets, and tables**. The project is `ncssm-price-transparency`. There are three datasets:
  * `hospital_data` contains data from each hospital that's available. The tables are named `hospital_N` for some number `N` for each hospital. See the contents of the table to get the hospital information. You only have read access to this data.
  * `turquoise` contains data from the Turquoise Health dataset. It has been unaltered as much as possible. There is only one table you should care about in that dataset: `turquoise-health-data`. You only have read access to this data.
  * `ad_hoc` is a dataset that you can use collectively to create intermediate datasets. You have full access to all tables created in this dataset, including those created by others! 

Here are a few starter queries to get an understanding of what to do. There are plenty of SQL or BigQuery tutorials online, and you can access this data from Jupyter notebooks and other common methods as well.

See a row from a specific hospital table:
```
SELECT
  *
FROM
  `ncssm-price-transparency.hospital_data.hospital_0`
LIMIT 1
```

See the ID --> Hospital mapping (this utilizes [BigQuery wildcard syntax](https://cloud.google.com/bigquery/docs/querying-wildcard-tables):
```
SELECT DISTINCT
  id,
  hospital_name
FROM
  `ncssm-price-transparency.hospital_data.hospital_*`
ORDER BY
  id
```

