# LMF Step 2 Execution Plan: Meta Ads Experiment

이 문서는 `LMF_Agent_Guide.md` 및 `LMF_Step1_Report_NA.md`에서 수립한 가설을 **Meta Ads(Facebook/Instagram)** 플랫폼에서 검증하기 위한 구체적인 실행 계획 및 기술적 가이드입니다.

---

## 1. Targeting Keywords (for MCP/API)

각 페르소나에 도달하기 위해 Meta Ads API에서 사용할 **관심사(Interests)** 키워드 리스트입니다.
MCP의 `mcp_meta_ads_search_interests` 기능을 통해 검증된 키워드 후보입니다.

### Persona A: Gen Z "FinTok" (Education/Hacks)
*   **Core Keywords:**
    *   `Personal finance`
    *   `Financial literacy`
    *   `Student loans`
    *   `Credit score`
    *   `Side hustle`
    *   `Passive income`
*   **Demographics:**
    *   Age: 18-24
    *   Location: United States, Canada
    *   Language: English (US)

### Persona B: Millennial "Professional" (Efficiency) - **Priority Target**
*   **Core Keywords:**
    *   `Investment`
    *   `Exchange-traded fund (ETF)`
    *   `Real estate investing`
    *   `Financial independence`
    *   `Morning Brew` (if available as interest)
    *   `Bloomberg`
    *   `The Wall Street Journal`
*   **Demographics:**
    *   Age: 25-40
    *   Location: United States, Canada
    *   Language: English (US)

### Persona C: Active Trader (FOMO/Signal)
*   **Core Keywords:**
    *   `Day trading`
    *   `Technical analysis`
    *   `Stock market`
    *   `Cryptocurrency`
    *   `Options (finance)`
    *   `Robinhood (company)`
*   **Demographics:**
    *   Age: 21-45
    *   Location: United States
    *   Language: English (US)

---

## 2. Ad Creatives & Copywriting

각 가설(Hypothesis)에 맞춰 준비된 영어 광고 카피입니다.

### Type A (Hypothesis 1: Efficiency) - **MAIN TEST**
*   **Concept:** "Market in a minute"
*   **Headline:** Market recap in 60s. ⏱️
*   **Primary Text:** Stop doomscrolling. Start earning. 
    
    Get your daily market brief while you brew your coffee. 
    No jargon, just the signals you need to know today.
    
    👇 Join the waitlist for early access.
*   **Call to Action:** Sign Up

### Type B (Hypothesis 2: Education)
*   **Concept:** "Money Hacks"
*   **Headline:** 30s Money Hacks 💸
*   **Primary Text:** Your school didn't teach you this about taxes. 
    
    Learn finance like you scroll TikTok. 
    Swipe to see how to fix your credit score in 3 steps.
*   **Call to Action:** Learn More

### Type C (Hypothesis 3: FOMO)
*   **Concept:** "Don't Miss Out"
*   **Headline:** Don't miss the next rally. 🚀
*   **Primary Text:** Did you miss NVDA? 
    
    Get top 1% trader insights and signals before the market moves. 
    See what the whales are buying right now.
*   **Call to Action:** Subscribe

---

## 3. Execution Script (Python)

MCP가 아직 연동되지 않았거나, 직접 스크립트로 제어하고 싶을 때 사용할 수 있는 Python 코드 초안입니다.
`facebook_business` SDK를 사용합니다.

**Prerequisites:**
```bash
pip install facebook-business
```

**Script (`run_ads_experiment.py`):**

```python
import sys
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.adimage import AdImage
from facebook_business.adobjects.adcreative import AdCreative
from facebook_business.adobjects.ad import Ad

# --- CONFIGURATION ---
ACCESS_TOKEN = 'YOUR_ACCESS_TOKEN'
AD_ACCOUNT_ID = 'act_YOUR_ACCOUNT_ID'
APP_ID = 'YOUR_APP_ID'
APP_SECRET = 'YOUR_APP_SECRET'
PAGE_ID = 'YOUR_PAGE_ID' # Facebook Page ID associated with the ads

# Initialize API
FacebookAdsApi.init(APP_ID, APP_SECRET, ACCESS_TOKEN)
account = AdAccount(AD_ACCOUNT_ID)

def create_lmf_experiment():
    print("🚀 Starting LMF Ad Experiment Setup...")

    # 1. Create Campaign
    campaign = account.create_campaign(params={
        'name': 'LMF_Validation_US_Test_v1',
        'objective': 'OUTCOME_LEADS', # or OUTCOME_TRAFFIC
        'status': 'PAUSED', # Start paused for safety
        'special_ad_categories': [],
    })
    print(f"✅ Campaign Created: {campaign['id']}")

    # 2. Define Ad Sets (Targeting) - Example for Persona B (Millennials)
    adset_params = {
        'name': 'AdSet_Persona_B_Efficiency',
        'campaign_id': campaign['id'],
        'daily_budget': 3000, # 3000 cents = $30.00 USD
        'billing_event': 'IMPRESSIONS',
        'optimization_goal': 'LEAD_GENERATION',
        'bid_strategy': 'LOWEST_COST_WITHOUT_CAP',
        'targeting': {
            'geo_locations': {'countries': ['US', 'CA']},
            'age_min': 25,
            'age_max': 40,
            'publisher_platforms': ['instagram', 'facebook'],
            'facebook_positions': ['feed', 'story'],
            'instagram_positions': ['stream', 'story'],
            'interests': [
                {'id': '6003139266461', 'name': 'Investment'}, # IDs need to be searched via Search API
                {'id': '6003358043685', 'name': 'ETF'},
            ],
        },
        'status': 'PAUSED',
    }
    adset = account.create_ad_set(params=adset_params)
    print(f"✅ Ad Set Created: {adset['id']}")

    # 3. Upload Creative (Image)
    # image = account.create_ad_image(params={'filename': './ad_creative_type_a.jpg'})
    # image_hash = image['hash']
    # print(f"✅ Image Uploaded: {image_hash}")
    
    # Placeholder for image hash if file not present
    image_hash = 'INSERT_IMAGE_HASH_HERE' 

    # 4. Create Ad Creative (Copy + Visual)
    creative_params = {
        'name': 'Creative_Type_A_Efficiency',
        'object_story_spec': {
            'page_id': PAGE_ID,
            'instagram_actor_id': PAGE_ID, # Or specific IG User ID
            'link_data': {
                'image_hash': image_hash,
                'link': 'https://your-waitlist-url.com',
                'message': 'Stop doomscrolling. Start earning. Get your daily market brief while you brew your coffee.', # Primary Text
                'name': 'Market recap in 60s. ⏱️', # Headline
                'call_to_action': {
                    'type': 'SIGN_UP',
                    'value': {'link': 'https://your-waitlist-url.com'}
                }
            }
        }
    }
    creative = account.create_ad_creative(params=creative_params)
    print(f"✅ Creative Created: {creative['id']}")

    # 5. Create Ad
    ad_params = {
        'name': 'Ad_Type_A_Variant_1',
        'adset_id': adset['id'],
        'creative': {'creative_id': creative['id']},
        'status': 'PAUSED',
    }
    ad = account.create_ad(params=ad_params)
    print(f"✅ Ad Created: {ad['id']}")
    print("\n🎉 Setup Complete! Go to Ads Manager to review and publish.")

if __name__ == "__main__":
    # create_lmf_experiment()
    print("Please configure tokens and IDs in the script before running.")
```

---

## 4. MCP Instructions

MCP가 연결된 후, 에이전트에게 내릴 수 있는 구체적인 명령입니다.

**Step 1. 타겟팅 탐색**
> "북미(US) 타겟으로 'Investment', 'ETF', 'Financial independence'에 관심 있는 오디언스 사이즈와 관련 관심사 키워드 10개를 `mcp_meta_ads_search_interests`로 찾아줘."

**Step 2. 캠페인 생성**
> "캠페인 이름 'LMF_Validation_US'로 트래픽(TRAFFIC) 목표 캠페인을 만들어줘."

**Step 3. 광고 세트 생성**
> "방금 만든 캠페인 안에, 25-40세 미국 거주자 대상, 'Investment' 관심사 타겟, 일 예산 $30로 설정된 'AdSet_Millennial'을 만들어줘."

