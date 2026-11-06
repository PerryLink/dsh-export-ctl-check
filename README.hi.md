<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/dsh-export-ctl-check-hero-en-dark.webp">
  <img src="docs/assets/dsh-export-ctl-check-hero-en-light.webp" width="100%" alt="dsh-export-ctl-check: बाईं ओर प्लगइन का नाम, दो मूल्य-पंक्तियाँ और यह टिप्पणी है कि 8 नियम रजिस्टर का चक्र पूरा करते हैं और कोई नियंत्रण-सूची नहीं रखी जाती; दाईं ओर एक वस्तु का स्कोरबोर्ड है — आठ खाने, हर नियम के लिए एक, जिसमें नियम का id, वह कॉलम जिसे वह पढ़ता है और देखा गया मान है (controlled खाली → हिट; licenseNo की शर्त पूरी नहीं → छोड़ा; licenseAt भरा → उत्तीर्ण; endUse/endUser भरे → उत्तीर्ण; destination भरा → उत्तीर्ण; licenseNo बिना दोहराव → उत्तीर्ण; category civil-military, मान कॉन्फ़िगर नहीं → छोड़ा; itemName साफ़ → उत्तीर्ण), और नीचे EC-001 की एक warn प्राप्ति तथा EC-002 व EC-007 के दो छोड़े गए नियम उनके कारण के साथ">
</picture>

# dsh-export-ctl-check

**निर्यात-नियंत्रण वस्तु रजिस्टर को पंक्ति-दर-पंक्ति जाँचें — कौन-सी पंक्ति, कौन-सा कॉलम, क्या छूटा। केवल अंतर, कोई निर्णय नहीं।**

सीमा-शुल्क अनुपालन और निर्यात-नियंत्रण टीमों के लिए एक ऑफ़लाइन जाँचकर्ता: यह एक वस्तु रजिस्टर (निर्यातक हेडर और प्रति वस्तु एक पंक्ति) पढ़ता है और संस्करणबद्ध नियम-पैक के अनुसार उसी रजिस्टर की पूर्णता और क्लोज़र जाँचता है। कोई नेटवर्क नहीं, कोई मॉडल कॉल नहीं, मूल सामग्री में कोई बदलाव नहीं।

[इंस्टॉल](#तीन-चरणों-में-शुरुआत) · [कॉन्फ़िगरेशन](#कॉन्फ़िगरेशन) · [FAQ](#faq) · [简体中文](README.md) · [English](README.en.md) · [Español](README.es.md) · [Português](README.pt.md) · [हिन्दी](README.hi.md)

[![License](https://img.shields.io/badge/license-Apache--2.0-3366CC?style=flat-square&labelColor=2B3245)](LICENSE)
[![DSH](https://img.shields.io/badge/DSH-%E2%89%A50.2.1%20%3C0.3.0-4B67B4?style=flat-square&labelColor=2B3245)](#संगतता)
[![npm](https://img.shields.io/npm/v/dsh-export-ctl-check?style=flat-square&labelColor=2B3245&color=CB3837)](https://www.npmjs.com/package/dsh-export-ctl-check)
[![CI](https://img.shields.io/github/actions/workflow/status/PerryLink/dsh-export-ctl-check/ci.yml?branch=main&label=CI&style=flat-square&labelColor=2B3245)](https://github.com/PerryLink/dsh-export-ctl-check/actions/workflows/ci.yml)
[![Node](https://img.shields.io/badge/node-%5E22.19%20%7C%7C%20%3E%3D24-339933?style=flat-square&labelColor=2B3245)](#संगतता)

[![Stars](https://img.shields.io/github/stars/PerryLink/dsh-export-ctl-check?style=flat-square&labelColor=2B3245)](https://github.com/PerryLink/dsh-export-ctl-check/stargazers)
[![npm downloads](https://img.shields.io/npm/dm/dsh-export-ctl-check?style=flat-square&labelColor=2B3245&color=CB3837)](https://www.npmjs.com/package/dsh-export-ctl-check)
[![dshfind](https://dshfind.com/api/badge/PerryLink/dsh-export-ctl-check?metric=downloads)](https://dshfind.com/plugins/PerryLink/dsh-export-ctl-check?ref=badge)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/PerryLink/dsh-export-ctl-check/badge)](https://securityscorecards.dev/viewer/?uri=github.com/PerryLink/dsh-export-ctl-check)
[![DSH Market](https://img.shields.io/badge/DSH_Market-listed-4B67B4?style=flat-square&labelColor=2B3245)](https://dsh.market/)
[![Gitee](https://img.shields.io/badge/Gitee-mirror-C71D23?style=flat-square&labelColor=2B3245&logo=gitee)](https://gitee.com/perrylink/dsh-export-ctl-check)

```sh
dsh plugin --profile <name> add dsh-export-ctl-check
```

</div>

<sub>समुदाय प्लगइन, DeepSeek से संबद्ध नहीं। मानक रिपॉज़िटरी: <https://github.com/PerryLink/dsh-export-ctl-check> (Gitee एक मिरर है)।</sub>

## यह क्या है

`dsh-export-ctl-check` एक निर्यात-नियंत्रण वस्तु रजिस्टर पढ़ता है — निर्यातक हेडर और प्रति वस्तु एक पंक्ति — और वस्तुओं पर कोई निर्णय दिए बिना उसी रजिस्टर की पूर्णता और क्लोज़र जाँचता है: क्या हर वस्तु नियंत्रण कॉलम में लिखती है कि वह नियंत्रित है या नहीं, क्या नियंत्रित के रूप में चिह्नित वस्तु के पास निर्यात लाइसेंस संख्या है, क्या दर्ज लाइसेंस संख्या के साथ जारी करने की तारीख है, क्या अंतिम उपयोग या अंतिम उपयोगकर्ता दर्ज है, क्या अंतिम गंतव्य दर्ज है, क्या एक ही रजिस्टर में लाइसेंस संख्या दोहराई गई है, क्या नियंत्रण श्रेणी संस्था की अपनी सूची से ली गई है, और क्या वस्तु-नाम कॉलम में कोई भरा न गया टेम्पलेट प्लेसहोल्डर बचा है।

यह केवल वे अंतर गिनाता है जिन्हें सामग्री के भीतर इंगित किया जा सकता है, और हर अंतर के लिए पंक्ति, कॉलम, क्या छूटा और क्या भरना है बताता है; यह तय नहीं करता कि कोई वस्तु नियंत्रित है या नहीं, लाइसेंस आवश्यक है या नहीं, या कोई निर्यात नियमों का उल्लंघन करता है या नहीं। चैट में सामग्री सौंप दें — इंस्टॉल एक ही कमांड है और निष्कर्ष सीधे पढ़े जाते हैं। 33 टेस्ट (`npx vitest run`) सभी 8 नियमों के युग्मित फ़िक्सचर कवर करते हैं, और `samples/quickstart` ऑफ़लाइन एक वास्तविक जाँच चलाता है।

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/dsh-export-ctl-check-flow-v5-dark.svg">
  <img src="docs/assets/dsh-export-ctl-check-flow-v5-light.svg" width="100%" alt="dsh-export-ctl-check संरचना: बाईं ओर दो इनपुट — रजिस्टर (JSON/YAML: चार वैकल्पिक हेडर फ़ील्ड, rows[], 13 मानक कॉलम और उनके alias, requireAnyOf) और नियम-पैक (8 नियम, 6 प्रकार की जाँच, लोड के समय सत्यापित) — तथा वह सीमा जिसे यह पार नहीं करता (कोई नियंत्रण-सूची नहीं); बीच में आठ द्वार एक सीढ़ी में, पहले तीन शर्त-श्रृंखला controlled → licenseNo → licenseAt बनाते हैं और हर द्वार केवल एक निकास से बाहर जाता है; दाईं ओर दो निकास और एक रिपोर्ट — issues[] (एक warn: पंक्ति 1 में controlled खाली, expected, fix और locator के साथ) और skipped[] (EC-002, EC-007 अपने कारण के साथ) — जो error 0 / warn 1 / info 0, issues 1, markdown और reportJson में मिलते हैं">
</picture>

## तीन चरणों में शुरुआत

1. **इंस्टॉल करें** (कोई एक चैनल चुनें):

   ```sh
   # git चैनल (नवीनतम main)
   dsh plugin --profile web add github:PerryLink/dsh-export-ctl-check
   # npm चैनल (प्रकाशित संस्करण)
   dsh plugin --profile web add dsh-export-ctl-check
   # tarball चैनल: इस रिपॉज़िटरी में pnpm pack के बाद
   dsh plugin --profile web add ./dsh-export-ctl-check-<version>.tgz
   ```

   कोई रनटाइम निर्भरता नहीं; `lib/index.mjs` और `rules/` ही प्रकाशित आर्टिफ़ैक्ट हैं।

2. **न्यूनतम कॉन्फ़िग** (डिफ़ॉल्ट ही काम करते हैं; नियम-पैक पैकेज के साथ आता है):

   ```yaml
   - insert:
       - id: dsh-export-ctl-check
         name: dsh-export-ctl-check
   ```

3. **जाँचें कि यह माउंट हुआ**:

   ```sh
   dsh --profile web --dump-config | grep 'dsh-export-ctl-check'
   node samples/quickstart/run.mjs
   ```

   ```text
   $ node samples/quickstart/run.mjs
   export_ctl_check: 1 issue(s) — error 0, warn 1, info 0
   skipped: 2
   ```

**अनइंस्टॉल**: `dsh plugin --profile web remove dsh-export-ctl-check` (या प्रोफ़ाइल पैच से वह पंक्ति हटा दें)।

> प्लगइन कोई नेटवर्क अनुरोध नहीं करता और सामग्री फ़ाइल नहीं लिखता; पूरी जाँच स्थानीय रहती है। नमूना `samples/quickstart/input/` में और अपेक्षित आउटपुट `samples/quickstart/expected/result.json` में है। WorkBuddy / Coze में Customs Compliance Suite भी खोजा जा सकता है (यह जाँच उसका एक हिस्सा है; उपलब्धता उस स्टोर में सूचीबद्ध होने के अनुसार है)।

## मुख्य क्षमताएँ

`export_ctl_check` की एक ही टूल सतह है: सामग्री पढ़ो, नियम-पैक चलाओ, एक रिपोर्ट लौटाओ। क्षमताएँ, इस आधार पर कि आपको क्या मिलता है:

- **एक ही बार में आठ नियम** — `EC-001` से `EC-008` नियंत्रण घोषणा, लाइसेंस संख्या, जारी तिथि, अंतिम उपयोग और अंतिम उपयोगकर्ता, गंतव्य, दोहराई गई लाइसेंस संख्या, नियंत्रण श्रेणी और वस्तु-नाम प्लेसहोल्डर को कवर करते हैं। हर नियम जाँचता है कि कुछ भरा गया है या नहीं, यह नहीं कि वह सही है या नहीं।
- **पंक्ति और कॉलम तक स्थान** — हर फ़ाइंडिंग में `locator` (`row` + `field`), `found`, `expected` और `fix` होते हैं, इसलिए आप सीधे रजिस्टर के उसी सेल पर लौट सकते हैं।
- **छोड़ी गई जाँच को कारण बताना होता है** — जो जाँच नहीं चल सकतीं वे कारण के साथ `skipped` में जाती हैं; खाली समस्या-सूची का अर्थ "सब ठीक है" नहीं है, और बिना कॉन्फ़िगर किया गया नियम या अनुपस्थित कॉलम चुपचाप सफलता नहीं पढ़ा जाता।
- **नियम डेटा हैं** — नियम-पैक `rules/export-ctl-check.yaml` कोड से अलग है; फ़ाइल बदलने से TypeScript छुए बिना नियम-सेट संस्करण बदल जाता है। लोडर हर नियम के `document` / `number` / `clause` / `excerpt` / `kind` / `source` को सत्यापित करता है।
- **कोई गढ़ा हुआ हवाला नहीं** — उद्धरण शब्दशः होना चाहिए; जब आधार केवल सिद्धांत हो तो `kind` `derived-from-principle` रहता है और गंभीरता `warn` तक सीमित रहती है, जबकि संस्था-निर्धारित सीमा `info` तक।
- **पूरी तरह ऑफ़लाइन** — कोई नेटवर्क अनुरोध, कोई मॉडल कॉल और रजिस्टर में कोई लेखन नहीं; टूल टेक्स्ट रिपोर्ट (`markdown`) और संरचित रिपोर्ट (`reportJson`) लौटाता है।

### नियम तालिका

| नियम | क्या जाँचता है | गंभीरता | आधार प्रकार |
|---|---|---|---|
| `EC-001` | हर वस्तु लिखती है कि वह नियंत्रित है या नहीं | `warn` | सिद्धांत से व्युत्पन्न |
| `EC-002` | नियंत्रित वस्तु के पास लाइसेंस संख्या है | `warn` | प्रत्यक्ष |
| `EC-003` | दर्ज लाइसेंस के साथ जारी तिथि है | `warn` | सिद्धांत से व्युत्पन्न |
| `EC-004` | अंतिम उपयोग या अंतिम उपयोगकर्ता दर्ज है | `warn` | प्रत्यक्ष |
| `EC-005` | गंतव्य दर्ज है | `warn` | प्रत्यक्ष |
| `EC-006` | लाइसेंस संख्याएँ रजिस्टर में दोहराई नहीं जातीं | `warn` | सिद्धांत से व्युत्पन्न |
| `EC-007` | नियंत्रण श्रेणी आपकी सूची से आती है | `info` | सिद्धांत से व्युत्पन्न |
| `EC-008` | वस्तु-नाम में कोई अनबदला प्लेसहोल्डर नहीं बचता | `warn` | प्रत्यक्ष |

### उदाहरण

यह प्लगइन के अपने `EC-001` फ़िक्सचर पर वास्तविक आउटपुट है, कोई चित्रण नहीं।

**टूल** `export_ctl_check`

**इनपुट**

~~~json
{"rows":[{"物项名称":"某型高性能传感器","是否受控":""}]}
~~~

**आउटपुट**

~~~json
{
  "id": "dsh-export-ctl-check.EC-001.de09b5a6",
  "ruleId": "EC-001",
  "severity": "warn",
  "locator": {
    "field": "controlled",
    "row": 1
  },
  "found": "第 1 行「controlled」为空",
  "expected": "「controlled」应填写",
  "fix": "补填是否受控；本条只核对是否声明，不判断该判断是否正确"
}
~~~

*Observed from `tests/fixtures/EC-001/EC-001-unsafe.json (cases.json expects EC-001 count 1); run via lib/index.mjs rules/export-ctl-check.yaml`*

### आप क्या पूछते हैं, यह क्या उत्तर देता है

| आप पूछते हैं | यह क्या उत्तर देता है |
|---|---|
| कोई वस्तु नियंत्रित के रूप में चिह्नित है पर लाइसेंस संख्या नहीं है। क्या यह रिपोर्ट होता है? | हाँ, `EC-002` यह कमी रिपोर्ट करता है: जब किसी पंक्ति का नियंत्रण मान उन मानों में हो जिन्हें नियम नियंत्रित मानता है, तो वह निर्यात लाइसेंस संख्या माँगता है। नियम केवल यह जाँचता है कि संख्या भरी गई है; यह नहीं जाँचता कि लाइसेंस असली है, वैध है, या उस वस्तु और गंतव्य को कवर करता है। यदि आपका रजिस्टर नियंत्रित के लिए कोई और शब्द लिखता है तो उसे नियम के शर्त मानों में जोड़ें, अन्यथा वह पंक्ति अनियंत्रित मानी जाएगी और नियम चुप रहेगा — इस प्लगइन के पास कोई नियंत्रण सूची नहीं है जो आपके लिए यह तय करे। |
| वस्तु बताती है कि वह नियंत्रित है या नहीं, पर अंतिम उपयोग और अंतिम उपयोगकर्ता दोनों खाली हैं। क्या यह पकड़ा जाता है? | हाँ, `EC-004` उस पंक्ति को रिपोर्ट करता है: वह इन दो कॉलमों में से कम-से-कम एक भरा होना माँगता है। एक पर्याप्त है, और नियम यह नहीं जाँचता कि बताया गया उपयोग या उपयोगकर्ता सच है या कानून द्वारा प्रतिबंधित है। |
| लाइसेंस संख्या लिखी है पर जारी तिथि का कॉलम खाली है। क्या यह फ़ाइंडिंग है? | `EC-003` तिथि माँगता है। शर्त लाइसेंस संख्या है: बिना संख्या वाली पंक्ति से तिथि नहीं माँगी जाती। नियम लाइसेंस की वैधता अवधि नहीं जाँचता और जारी तिथि की तुलना निर्यात तिथि से नहीं करता — वह केवल स्थापित करता है कि तिथि मौजूद है, यह नहीं कि वह पहले है। |
| एक ही लाइसेंस संख्या कई पंक्तियों में आती है। जाँच क्या कहती है? | `EC-006` उस संख्या को रजिस्टर में दोहराई गई बताता है। वह एक लाइसेंस द्वारा कई वस्तुओं को कवर करने — रजिस्टर रखने का सामान्य तरीका — और गलती से कॉपी की गई संख्या में अंतर नहीं कर सकता, इसलिए हिट की पुष्टि मनुष्य को करनी होती है; नियम कुछ भी पुनःक्रमांकित नहीं करता और यह भी नहीं बताता कि एक लाइसेंस कितनी पंक्तियों में हो सकता है। यदि आपका रजिस्टर जानबूझकर एक-लाइसेंस-कई-वस्तु के रूप में है तो उस लाइसेंस की पंक्तियों को क्रमांक दें, या नियम बंद करें। |
| किसी पंक्ति में अंतिम गंतव्य ही नहीं है। | `EC-005` उसे रिपोर्ट करता है, क्योंकि हर वस्तु को गंतव्य ले जाना होता है। वह केवल यह जाँचता है कि कॉलम भरा है, यह नहीं कि गंतव्य अनुमत है: कोई देश या क्षेत्र प्रतिबंधित है या नहीं, यह सक्षम प्राधिकरण की प्रकाशित सूचियों से पढ़ा जाता है, और इस प्लगइन में कोई देश-सूची नहीं है। |
| वस्तु-नाम कॉलम में अब भी कोई उदाहरण मान या `XXX` लिखा है — यह दोष है या असली नाम? | जब नाम में नियम द्वारा खोजे जाने वाले शब्दों में से कोई हो तो `EC-008` उस पंक्ति को रिपोर्ट करता है: कोष्ठक में प्लेसहोल्डर, `XXX`, `xxx`, `TBD`, `todo`, या "भरें" जैसा चिह्न। वह शब्द-सूची आपके अपने टेम्पलेट के अनुसार है और बदली जा सकती है। नियम उन शब्दों को केवल उसी एक कॉलम में खोजता है: वह कभी नहीं जाँचता कि नाम तथ्यात्मक रूप से सही है या नहीं। |

## कॉन्फ़िगरेशन

सभी समायोज्य पैरामीटर `src/config.ts` के Schemastery स्कीमा में हैं, इसलिए कोड छुए बिना `cordis.yml` से बदले जा सकते हैं; प्रति-नियम सीमाएँ `rules/` के नियम-पैक में हैं।

| कुंजी | प्रकार | डिफ़ॉल्ट | अर्थ |
|---|---|---|---|
| `rulesFile` | string | `rules/export-ctl-check.yaml` | नियम-पैक पथ, पैकेज रूट के सापेक्ष |
| `disabledRules` | string[] | `[]` | रोके जाने वाले नियम id; हर एक `skipped` में आता है |
| `onlyRules` | string[] | `[]` | केवल ये नियम चलाएँ; खाली का अर्थ सभी नियम |
| `skipNotes` | string | `""` | हर `skipped` कारण के साथ जोड़ा जाने वाला नोट |
| `timeoutMs` | number | `120000` | टूल का सहकारी टाइमआउट बजट |

<details>
<summary>नियम-स्तरीय पैरामीटर (नियम-पैक में, यहाँ नहीं)</summary>

- `EC-002` `conditionValues` — नियंत्रण कॉलम के कौन-से मान किसी वस्तु को नियंत्रित मानते हैं। फ़ैक्टरी डिफ़ॉल्ट ये हैं:

```text
是 · Y · yes · true · 受控 · √
```

  यदि आपका रजिस्टर कोई और रूप लिखता है तो उसे इस सूची में जोड़ें; अन्यथा पंक्ति अनियंत्रित गिनी जाएगी और नियम चुप रहेगा।
- `EC-007` `values` — आपकी संस्था की नियंत्रण श्रेणियाँ, उदाहरण `[nuclear, missile, biological, chemical, dual-use]`। खाली का अर्थ "कॉन्फ़िगर नहीं" है और नियम स्वयं को `skipped` में बताता है; प्लगइन कोई वर्गीकरण कठोर-कोड नहीं करता।
- `EC-008` `terms` — खोजे जाने वाले टेम्पलेट शब्द। फ़ैक्टरी डिफ़ॉल्ट ये हैं:

```text
【 】 {{ }} XXX xxx 待填 待补充 TBD todo 示例
```

</details>

प्रोफ़ाइल पैच में ओवरराइड का उदाहरण:

```yaml
- insert:
    - id: dsh-export-ctl-check
      name: dsh-export-ctl-check
      config:
        onlyRules: [EC-001, EC-002, EC-003]
        skipNotes: संस्था नियम, 2026 संस्करण
```

## सामग्री प्रारूप

टूल JSON या YAML स्वीकार करता है। इनपुट `file` (सामग्री फ़ाइल का निरपेक्ष पथ) या `material` (इनलाइन टेक्स्ट) में से ठीक एक होता है। Excel को पहले JSON/YAML में बदला जा सकता है, चैट में भी यदि प्लेटफ़ॉर्म अनुमति दे।

```yaml
exporter: 某某进出口有限公司
contractNo: SC-2026-018
listVersion: 2026 年版
rows:
  - { 序号: '1', 物项名称: 某型高性能传感器, 商品编号: '9031809090',
      管制类别: 军民两用, 最终用途: 用于工业自动化产线的位移测量,
      最终用户: 某某工业自动化有限公司, 最终目的地: 德国,
      许可证号: EX2026-0018, 许可日期: 2026-02-25, 是否受控: 是 }
```

कॉलम नाम बड़े-छोटे अक्षरों में अंतर किए बिना और स्थान, अंडरस्कोर तथा हाइफ़न छोड़कर मिलाए जाते हैं; रजिस्टर के अपने कॉलम नाम सुरक्षित रहते हैं, इसलिए हर फ़ाइंडिंग उस कॉलम का नाम लेती है जिसे उसने पढ़ा। फ़ील्ड पढ़ने की परत में वैकल्पिक हैं और जाँच इंजन उन्हें सत्यापित करता है, इसलिए आंशिक निर्यात "कमी" वाली फ़ाइंडिंग देता है, क्रैश नहीं।

## मानक जिनका पालन होता है

| दस्तावेज़ | संख्या | इसे उद्धृत करने वाले नियम |
|---|---|---|
| जनवादी गणराज्य चीन का निर्यात नियंत्रण कानून | 17 अक्टूबर 2020 को 13वीं राष्ट्रीय जन कांग्रेस की स्थायी समिति के 22वें सत्र में पारित, राष्ट्रपति आदेश संख्या 58 द्वारा प्रकाशित, 1 दिसंबर 2020 से प्रभावी | EC-001, EC-002, EC-003, EC-004, EC-005, EC-006, EC-008 |
| जनवादी गणराज्य चीन का निर्यात नियंत्रण कानून | वर्तमान संस्करण इस बार सत्यापित नहीं | EC-007 |

**सीमा:** यह प्लगइन एक **निर्यात-नियंत्रण वस्तु रजिस्टर** को उस बंद चक्र के लिए जाँचता है जो रजिस्टर से अपेक्षित है — कि हर वस्तु बताए कि वह नियंत्रित है या नहीं, नियंत्रित वस्तु के पास लाइसेंस संख्या हो, लाइसेंस के साथ जारी तिथि हो, अंतिम उपयोग या अंतिम उपयोगकर्ता दर्ज हो, गंतव्य दर्ज हो, लाइसेंस संख्याएँ न दोहराई जाएँ, नियंत्रण श्रेणी आपकी सूची से आए और कोई प्लेसहोल्डर न बचे। यह **यह नहीं** तय करता कि कोई वस्तु नियंत्रित है, लाइसेंस आवश्यक है, या कोई निर्यात नियम तोड़ेगा।

### नियम-पैक

नियम डेटा `rules/export-ctl-check.yaml` में है। उसका हेडर बताता है कि प्लगइन के पास कोई नियंत्रण सूची नहीं है और वह सूची-खोज नहीं करता, इसलिए वह घोषित न किए गए नियंत्रित वस्तु को नहीं पकड़ सकता। लोड-टाइम गार्ड फिर भी हर नियम के लिए दस्तावेज़, खंड, उद्धरण और स्रोत माँगता है, और सिद्धांत-व्युत्पन्न या स्थानीय-कॉन्फ़िगर जाँच को `error` होने से रोकता है।

> ### ⚠️ रिपोर्ट के किसी हवाले पर भरोसा करने से पहले यह पढ़ें
>
> **`excerpt` की स्थिति प्रति-नियम है, एकसमान नहीं।** कुछ नियम खंड को शब्दशः उद्धृत करते हैं (`kind: direct`), कुछ उद्धृत अनुच्छेदों के सिद्धांत से व्युत्पन्न हैं (`kind: derived-from-principle`, अधिकतम `warn`), और कुछ में सीमाएँ आपकी संस्था निर्धारित करती है (`kind: institutional-configuration`, अधिकतम `info`)। पैक कभी उद्धरण का पैराफ़्रेज़ नहीं करता: जब पाठ नहीं मिला तो `excerpt` स्वयं यह बताता है और तर्क `note` में रहता है; एक टेस्ट जाँचता है कि कोई नियम ऐसा उद्धरण नहीं माँगता जो उसके पास नहीं है। **जो नियम अब भी "पाठ नहीं मिला" के रूप में चिह्नित हैं, उनके लिए पाठ मिलने पर `excerpt` को असली खंड से बदलें और `kind` को `direct` तक बढ़ाएँ।**
>
> निष्कर्ष समीक्षक का है: यह प्लगइन केवल वे अंतर गिनाता है जिन्हें सामग्री में इंगित किया जा सकता है, और तथ्य या अनुपालन तय नहीं करता।

## FAQ

<details>
<summary>क्या सामग्री अपलोड होती है या नेटवर्क से संसाधित होती है?</summary>

नहीं। प्लगइन केवल वही पढ़ता है जो आप `file` या `material` से देते हैं, उसे स्थानीय रूप से पार्स करता है और नियम स्थानीय रूप से चलाता है: कोई नेटवर्क अनुरोध नहीं, कोई टेलीमेट्री नहीं, कोई मॉडल कॉल नहीं। परिणाम केवल टूल के रिटर्न मान और DSH होस्ट के अपने सत्र लॉग में रहता है; पैकेज दूसरी प्रति नहीं रखता।

</details>

<details>
<summary>मुझे लगता है कोई वस्तु नियंत्रित होनी चाहिए पर कुछ रिपोर्ट नहीं हुआ। क्या यह चूक है?</summary>

यह प्लगइन की सबसे महत्वपूर्ण सीमा है, चूक नहीं: इसके पास नियंत्रण सूची नहीं है और यह किसी वस्तु-कोड या तकनीकी पैरामीटर को सूची प्रविष्टि से नहीं जोड़ता, इसलिए वह उस वस्तु को नहीं पकड़ सकता जिसे नियंत्रित घोषित होना चाहिए था पर हुआ नहीं। कोई वस्तु नियंत्रित है या नहीं, यह निर्णय प्रकाशित सूची के सामने निर्यातक का है। प्लगइन जो सुनिश्चित करता है वह यह है कि जो जाँच नहीं चल सकतीं वे `skipped` में जाती हैं, चुपचाप पास नहीं होतीं।

</details>

<details>
<summary>क्या यह अन्य प्लगइनों से कमांड नाम, इवेंट या स्लॉट के लिए टकराता है?</summary>

नहीं। यह केवल `tools` निर्भरता घोषित करता है और एक ही `export_ctl_check` टूल पंजीकृत करता है; कोई कमांड, क्लाइंट स्लॉट, `webServer` प्रीफ़िक्स पंजीकृत नहीं करता, कोई service key नहीं देता और कोई ग्लोबल नहीं बदलता। बिंदु-दर-बिंदु तर्क "इंटरऑपरेबिलिटी" में है।

</details>

<details>
<summary>प्रदर्शन लागत कितनी है?</summary>

स्थानीय पार्सिंग और नियम मिलान: कोई नेटवर्क नहीं, कोई मॉडल कॉल नहीं। डिफ़ॉल्ट टूल टाइमआउट बजट `120000` ms है। 33 टेस्ट (`npx vitest run`) सभी 8 नियमों के युग्मित फ़िक्सचर कवर करते हैं, और `samples/quickstart` ऑफ़लाइन दोबारा चलाया जा सकता है।

</details>

<details>
<summary>क्या नियम-पैक बदला जा सकता है?</summary>

हाँ। `rulesFile` किसी भी नियम-पैक फ़ाइल की ओर इंगित कर सकता है (पैकेज रूट के सापेक्ष या निरपेक्ष); नियम डेटा हैं और लोडर हवाले के फ़ील्ड तथा गंभीरता की सीमाएँ सत्यापित करता है। फ़ाइल बदलने से TypeScript छुए बिना नियम-सेट संस्करण बदल जाता है।

</details>

## सुरक्षा सीमाएँ

- **सामग्री केवल पढ़ी जाती है।** प्लगइन `file` या `material` से पढ़ता है, कभी वापस नहीं लिखता और मूल नहीं बदलता; एकमात्र लेखन DSH होस्ट का सत्र लॉग है, और पैकेज दूसरी प्रति नहीं जोड़ता।
- **कोई नेटवर्क नहीं, कोई मॉडल कॉल नहीं।** कोई नेटवर्क अनुरोध, कोई टेलीमेट्री और कोई मॉडल कॉल नहीं; पूरी जाँच स्थानीय है।
- **कोई निर्णायक भाषा नहीं।** रिपोर्ट सामग्री और उद्धृत खंडों के बीच शाब्दिक अंतर गिनाती है; वह अनुपालन, दायित्व या तथ्य की सत्यता का निर्णय नहीं करती। निष्कर्ष समीक्षक का है।
- **विफलता चुप नहीं रहती।** नियम-पैक लोड पर सत्यापित होता है; जो जाँच नहीं चल सकतीं वे कारण के साथ `skipped` में जाती हैं, और खाली समस्या-सूची कभी "कुछ गलत नहीं है" के रूप में नहीं पढ़ी जाती।
- **कोई गढ़ा हुआ हवाला नहीं।** उद्धरण शब्दशः होना चाहिए; जब पाठ नहीं मिल सकता तो पैक यह बताता है और गंभीरता सीमित करता है।
- **पंजीकरण एक effect है।** टूल पंजीकरण disposer लौटाता है, इसलिए रोकने या हॉट-रीलोड पर टूल हट जाता है और कोई लटका हुआ श्रोता नहीं बचता।

## ज्ञात सीमाएँ

- **अंदर कोई नियंत्रण सूची नहीं।** नियंत्रण कॉलम रजिस्टर की अपनी घोषणा है; प्लगइन केवल उस घोषणा के बाद का क्लोज़र जाँचता है और घोषित न किए गए नियंत्रित वस्तु को नहीं पकड़ सकता। यह प्लगइन की सबसे महत्वपूर्ण क्षमता-सीमा है।
- **लाइसेंस का स्वयं निर्णय नहीं।** `EC-002` और `EC-003` केवल जाँचते हैं कि संख्या और जारी तिथि भरी है; वे प्रामाणिकता, वैधता अवधि या उस वस्तु और गंतव्य के कवरेज को सत्यापित नहीं करते, और जारी तिथि की तुलना निर्यात तिथि से नहीं करते।
- **अंतिम उपयोग या अंतिम उपयोगकर्ता की सत्यता का निर्णय नहीं।** `EC-004` केवल दोनों में से कम-से-कम एक कॉलम भरा होना माँगता है; यह नहीं जाँचता कि बताया गया सच है या प्रतिबंधित है।
- **गंतव्य प्रतिबंधित है या नहीं, इसका निर्णय नहीं।** `EC-005` केवल जाँचता है कि गंतव्य कॉलम भरा है; कोई देश या क्षेत्र सूची अंदर नहीं है।
- **दोहराई गई लाइसेंस संख्या सुराग है, निष्कर्ष नहीं।** एक लाइसेंस कई वस्तुओं को कवर करता हो, यह रजिस्टर रखने का सामान्य तरीका है, इसलिए `EC-006` हिट की पुष्टि मनुष्य को करनी होती है; प्लगइन पुनःक्रमांकन नहीं करता और यह भी तय नहीं करता कि एक लाइसेंस कितनी पंक्तियों में हो सकता है।
- **`EC-007` को आपकी सूची चाहिए।** `values` खाली आता है, इसलिए कॉन्फ़िगर होने तक नियम स्वयं को `skipped` में बताता है; नियंत्रण श्रेणियों का विभाजन सूची संस्करण पर निर्भर है और प्लगइन कोई वर्गीकरण कठोर-कोड नहीं करता।
- **हवाले की स्थिति प्रति-नियम है।** कुछ नियम अब भी अपने `excerpt` को "पाठ नहीं मिला" बताते हैं, `kind: derived-from-principle` रखते हैं और `warn` तक सीमित रहते हैं; पाठ मिलने पर उद्धरण बदलें और प्रकार को `direct` तक बढ़ाएँ।
- **पूरा नियम-सेट अब भी 8 नियमों का है।** यह रजिस्टर-स्तरीय पूर्णता और क्लोज़र कवर करता है, वस्तु, लाइसेंस या लेन-देन की सारवान समीक्षा नहीं।

## इंटरऑपरेबिलिटी

प्लगइन एक टूल पंजीकृत करता है और अन्य प्लगइनों की सतह नहीं घेरता:

- **केवल `tools` निर्भरता।** `inject = ['tools']`; tools सेवा न होने पर कुछ पंजीकृत नहीं होता।
- **केवल `export_ctl_check`।** कोई कमांड, कोई क्लाइंट स्लॉट, कोई `webServer` प्रीफ़िक्स नहीं, इसलिए उन सीटों के लिए प्रतिस्पर्धा नहीं।
- **कोई service key नहीं, कोई ग्लोबल बदलाव नहीं।** कोई प्रोटोटाइप पैच नहीं, `process.env` में लेखन नहीं, ग्लोबल fetch का प्रतिस्थापन नहीं।
- **बंडल पैच केवल अपनी पंक्ति जोड़ता है।** `cordis.patch.yml` प्लगइन पंक्ति जोड़ता है और किसी अंतर्निहित पंक्ति का `config` कभी नहीं लिखता।
- **साझा किट अंदर कॉपी होता है।** `src/shared/` पैकेज में कॉपी किया गया साझा किट है, किसी अन्य प्लगइन की रनटाइम निर्भरता नहीं।
- **टूल पंजीकरण एक effect है।** `apply()` disposer लौटाता है, इसलिए रोकने या हॉट-रीलोड पर स्वच्छ रूप से हट जाता है।

## संगतता

| सतह | स्थिति |
|---|---|
| Harness | पीयर रेंज `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` — `0.2.0-rc.2` और `0.2.1-rc.2` दोनों स्वीकार करते हुए सत्यापित। `engines.dsh` को `>=0.2.1-0 <0.3.0` घोषित किया गया है और 0.2.1 से होस्ट इसे लागू करता है |
| Node | `^22.19.0 \|\| >=24.0.0` |
| प्लेटफ़ॉर्म | सभी (शुद्ध ESM; कोई नेटिव कोड नहीं, कोई नेटवर्क नहीं, कोई मॉडल कॉल नहीं) |
| टूल मोड | `native` और `ptc` दोनों में काम करता है; पूरी निर्देशिका के लिए `ptc` चुनें ताकि स्कीमा लागत एक बार दी जाए |

## समस्या निवारण

- **प्लगइन इंस्टॉल होता है पर टूल दिखता नहीं।** जाँचें कि `main` `lib/index.mjs` की ओर जाता है और `pnpm run build` ने उसे बनाया है; गलत `main` पर लोडर प्रविष्टि चुपचाप छोड़ देता है।
- **`dsh plugin add` पैकेज को असंगत बताकर अस्वीकार करता है।** पीयर रेंज `0.1.x` और `0.2.x` कवर करती है; यदि आपका रनटाइम उससे बाहर है तो स्पष्ट छूट दें: `dsh plugin --profile <name> allow-version dsh-export-ctl-check@0.1.0 --dsh-version <runtime> --accept-risk`।
- **मुझे लगता है कोई वस्तु नियंत्रित है पर रिपोर्ट नहीं हुई।** प्लगइन के पास नियंत्रण सूची नहीं है; प्रकाशित सूची के सामने स्वयं पुष्टि करें — "ज्ञात सीमाएँ" देखें।
- **`EC-002` उस वस्तु पर चलता है जो मुझे पता है अनियंत्रित है।** उसका नियंत्रण कॉलम कहता है कि वह नियंत्रित है; कॉलम सुधारें या लाइसेंस दर्ज करें — प्लगइन घोषणा पढ़ता है, माल नहीं।
- **`EC-006` एक लाइसेंस के कई वस्तुओं पर होने से चलता है।** उस लाइसेंस की पंक्तियों को क्रमांक दें, या नियम बंद करें।
- **`EC-005` नहीं जानता कौन-से गंतव्य प्रतिबंधित हैं।** वह केवल जाँचता है कि गंतव्य दर्ज है; देश-सूची जानबूझकर अंदर नहीं है।
- **कोई नियम नहीं चला।** `skipped` सरणी पढ़ें; वह नियम id और कारण बताती है।
- **`check` में `manifest-peers` विफल बताया जाता है।** स्थिर जाँचकर्ता 0.2 लाइन से पुरानी कठोर-कोडित पीयर रेंज से तुलना करता है; रनटाइम इंस्टॉल पर पीयर संगतता लागू करता है। यह `dsh-plugin-dev` की ज्ञात अपस्ट्रीम समस्या है।
- **समय खिसका हुआ लगता है।** सारी गणना दिए गए स्ट्रिंग पर वॉल-क्लॉक गणना है; कोई टाइमज़ोन रूपांतरण नहीं होता।

## इकोसिस्टम और गुणवत्ता

- [Gitee मिरर](https://gitee.com/perrylink/dsh-export-ctl-check) (सिंक मिरर; GitHub मानक है)
- [dshfind प्लगइन पेज](https://dshfind.com/plugins/PerryLink/dsh-export-ctl-check) (इंस्टॉल और रैंकिंग)
- [OpenSSF Scorecard रिपोर्ट](https://securityscorecards.dev/viewer/?uri=github.com/PerryLink/dsh-export-ctl-check) ([.github/workflows/scorecard.yml](.github/workflows/scorecard.yml) द्वारा संचालित)
- [DSH Market](https://dsh.market/) (सूचीबद्ध)
- [सामग्री के अनुसार जाँचकर्ता चुनें](https://perrylink.github.io/zh/checkers/choose/) (62 जाँचकर्ताओं और सामान्य प्लगइनों का चयन सूचकांक)

## डेवलपमेंट

```sh
pnpm install
pnpm run typecheck   # tsc --noEmit
pnpm test            # vitest, साझा टेबल सूट और युग्मित फ़िक्सचर
pnpm run build       # tsdown -> lib/index.mjs + lib/index.d.mts
pnpm run check:readmes
node ../scripts/sync-shared.mjs dsh-export-ctl-check
```

प्लगइन डेटा-आधारित है: `src/model.ts` तालिका का आकार घोषित करता है, `src/shared/` का साझा किट पाठक और जाँच इंजन देता है, और नियम-पैक हर जाँच घोषित करता है। अंतिम कमांड `../_shared` से साझा किट `src/shared/` में कॉपी करता है; साझा किट में हर बदलाव के बाद उसे दोबारा चलाएँ। README की छवियाँ [`scripts/gen-readme-assets.py`](scripts/gen-readme-assets.py) से प्रोग्रामेटिक रूप से बनती हैं (Python + Pillow: हल्का/गहरा hero WebP युग्म और हल्का/गहरा संरचना SVG युग्म) और दोबारा चलाई जा सकती हैं।

Topics: `dsh`, `dsh-plugin`, `deepseek-harness`, `cordis`, `export`, `ctl`

## परिवार और आभार

यह परियोजना [PerryLink](https://github.com/PerryLink) के DeepSeek Harness प्लगइन परिवार का हिस्सा है (सभी Apache-2.0)। यदि यह उपयोगी हो, तो **एक स्टार अगले व्यक्ति को इसे खोजने में मदद करता है** — इसके पीछे कोई सुविधा नहीं छिपी है।

- [@PerryLink](https://github.com/PerryLink) — निर्माता और अनुरक्षक: नियम-पैक, जाँच इंजन, युग्मित फ़िक्सचर और पाँच-भाषा दस्तावेज़।

<details>
<summary>सभी प्लगइन खोलें</summary>

| प्लगइन | स्थिति |
|---|---|
| **[dsh-aqua-input-check](https://github.com/PerryLink/dsh-aqua-input-check)** |  |
| **[dsh-archive-check](https://github.com/PerryLink/dsh-archive-check)** |  |
| **[dsh-auto-review](https://github.com/PerryLink/dsh-auto-review)** |  |
| **[dsh-autotier](https://github.com/PerryLink/dsh-autotier)** | 🧊 फ़्रोज़न — रेपो README देखें |
| **[dsh-bid-ca-precheck](https://github.com/PerryLink/dsh-bid-ca-precheck)** |  |
| **[dsh-bid-qual-check](https://github.com/PerryLink/dsh-bid-qual-check)** |  |
| **[dsh-cert-mcp](https://github.com/PerryLink/dsh-cert-mcp)** | 🧊 फ़्रोज़न — रेपो README देखें |
| **[dsh-checkpoint-rewind](https://github.com/PerryLink/dsh-checkpoint-rewind)** |  |
| **[dsh-click](https://github.com/PerryLink/dsh-click)** |  |
| **[dsh-composer-history](https://github.com/PerryLink/dsh-composer-history)** |  |
| **[dsh-contract-stance](https://github.com/PerryLink/dsh-contract-stance)** |  |
| **[dsh-customs-doc-check](https://github.com/PerryLink/dsh-customs-doc-check)** |  |
| **[dsh-data-quality](https://github.com/PerryLink/dsh-data-quality)** |  |
| **[dsh-demurrage-ledger](https://github.com/PerryLink/dsh-demurrage-ledger)** |  |
| **[dsh-doublecheck](https://github.com/PerryLink/dsh-doublecheck)** |  |
| **[dsh-drill-script-check](https://github.com/PerryLink/dsh-drill-script-check)** |  |
| **[dsh-eia-guide-check](https://github.com/PerryLink/dsh-eia-guide-check)** |  |
| **[dsh-emergency-plan](https://github.com/PerryLink/dsh-emergency-plan)** |  |
| **[dsh-essay-rubric-check](https://github.com/PerryLink/dsh-essay-rubric-check)** |  |
| **[dsh-evidence-check](https://github.com/PerryLink/dsh-evidence-check)** |  |
| **[dsh-export-ctl-check](https://github.com/PerryLink/dsh-export-ctl-check)** |  |
| **[dsh-fast](https://github.com/PerryLink/dsh-fast)** |  |
| **[dsh-fmea-table-check](https://github.com/PerryLink/dsh-fmea-table-check)** |  |
| **[dsh-forecast-penalty](https://github.com/PerryLink/dsh-forecast-penalty)** |  |
| **[dsh-fund-research](https://github.com/PerryLink/dsh-fund-research)** |  |
| **[dsh-github](https://github.com/PerryLink/dsh-github)** |  |
| **[dsh-gongwen-flow-check](https://github.com/PerryLink/dsh-gongwen-flow-check)** |  |
| **[dsh-gongwen-word-check](https://github.com/PerryLink/dsh-gongwen-word-check)** |  |
| **[dsh-guard-plan-qc](https://github.com/PerryLink/dsh-guard-plan-qc)** |  |
| **[dsh-hazchem-check](https://github.com/PerryLink/dsh-hazchem-check)** |  |
| **[dsh-hazplan-check](https://github.com/PerryLink/dsh-hazplan-check)** |  |
| **[dsh-hidden-risk-map](https://github.com/PerryLink/dsh-hidden-risk-map)** |  |
| **[dsh-hs-classify](https://github.com/PerryLink/dsh-hs-classify)** |  |
| **[dsh-icd-rule-check](https://github.com/PerryLink/dsh-icd-rule-check)** |  |
| **[dsh-industry-research](https://github.com/PerryLink/dsh-industry-research)** |  |
| **[dsh-lawcite-adapter](https://github.com/PerryLink/dsh-lawcite-adapter)** |  |
| **[dsh-laya](https://github.com/PerryLink/dsh-laya)** |  |
| **[dsh-lc-doc-check](https://github.com/PerryLink/dsh-lc-doc-check)** |  |
| **[dsh-learning-gap-check](https://github.com/PerryLink/dsh-learning-gap-check)** |  |
| **[dsh-library](https://github.com/PerryLink/dsh-library)** |  |
| **[dsh-local-ai](https://github.com/PerryLink/dsh-local-ai)** |  |
| **[dsh-lsp-actions](https://github.com/PerryLink/dsh-lsp-actions)** |  |
| **[dsh-mask](https://github.com/PerryLink/dsh-mask)** |  |
| **[dsh-mcp-panel](https://github.com/PerryLink/dsh-mcp-panel)** |  |
| **[dsh-medrec-qc](https://github.com/PerryLink/dsh-medrec-qc)** |  |
| **[dsh-memento](https://github.com/PerryLink/dsh-memento)** |  |
| **[dsh-nsfc-form-check](https://github.com/PerryLink/dsh-nsfc-form-check)** |  |
| **[dsh-nurse-record-check](https://github.com/PerryLink/dsh-nurse-record-check)** |  |
| **[dsh-observe](https://github.com/PerryLink/dsh-observe)** |  |
| **[dsh-origin-rvc-check](https://github.com/PerryLink/dsh-origin-rvc-check)** |  |
| **[dsh-ota-review-check](https://github.com/PerryLink/dsh-ota-review-check)** |  |
| **[dsh-output-styles](https://github.com/PerryLink/dsh-output-styles)** |  |
| **[dsh-paper-doc-adapter](https://github.com/PerryLink/dsh-paper-doc-adapter)** |  |
| **[dsh-permission-rules](https://github.com/PerryLink/dsh-permission-rules)** |  |
| **[dsh-permit-report-check](https://github.com/PerryLink/dsh-permit-report-check)** |  |
| **[dsh-pipeline-check](https://github.com/PerryLink/dsh-pipeline-check)** |  |
| **[dsh-pleading-draft](https://github.com/PerryLink/dsh-pleading-draft)** |  |
| **[dsh-plugin-doctor](https://github.com/PerryLink/dsh-plugin-doctor)** | 🚫 रिटायर्ड (रेपो संग्रहीत) |
| **[dsh-plugin-guide](https://github.com/PerryLink/dsh-plugin-guide)** |  |
| **[dsh-plugin-kit](https://github.com/PerryLink/dsh-plugin-kit)** | 🚫 रिटायर्ड (रेपो संग्रहीत) |
| **[dsh-plugin-upgrade](https://github.com/PerryLink/dsh-plugin-upgrade)** | 🚫 रिटायर्ड (रेपो संग्रहीत) |
| **[dsh-policy-brief-draft](https://github.com/PerryLink/dsh-policy-brief-draft)** |  |
| **[dsh-power-loss-split](https://github.com/PerryLink/dsh-power-loss-split)** |  |
| **[dsh-power-ticket-check](https://github.com/PerryLink/dsh-power-ticket-check)** |  |
| **[dsh-ppap-check](https://github.com/PerryLink/dsh-ppap-check)** |  |
| **[dsh-protest-deadline](https://github.com/PerryLink/dsh-protest-deadline)** |  |
| **[dsh-railway-window](https://github.com/PerryLink/dsh-railway-window)** |  |
| **[dsh-repair-order-qc](https://github.com/PerryLink/dsh-repair-order-qc)** |  |
| **[dsh-research-report](https://github.com/PerryLink/dsh-research-report)** |  |
| **[dsh-review-reply-check](https://github.com/PerryLink/dsh-review-reply-check)** |  |
| **[dsh-rulefile-check](https://github.com/PerryLink/dsh-rulefile-check)** |  |
| **[dsh-safety-brief-check](https://github.com/PerryLink/dsh-safety-brief-check)** |  |
| **[dsh-score](https://github.com/PerryLink/dsh-score)** |  |
| **[dsh-session-sync](https://github.com/PerryLink/dsh-session-sync)** |  |
| **[dsh-site-log-check](https://github.com/PerryLink/dsh-site-log-check)** |  |
| **[dsh-skill-pack-security](https://github.com/PerryLink/dsh-skill-pack-security)** |  |
| **[dsh-soe-decision-check](https://github.com/PerryLink/dsh-soe-decision-check)** |  |
| **[dsh-soilwater-check](https://github.com/PerryLink/dsh-soilwater-check)** |  |
| **[dsh-sop-sync-check](https://github.com/PerryLink/dsh-sop-sync-check)** |  |
| **[dsh-spc-gbt-adapter](https://github.com/PerryLink/dsh-spc-gbt-adapter)** |  |
| **[dsh-talk](https://github.com/PerryLink/dsh-talk)** |  |
| **[dsh-tender-extract](https://github.com/PerryLink/dsh-tender-extract)** |  |
| **[dsh-tender-matrix](https://github.com/PerryLink/dsh-tender-matrix)** |  |
| **[dsh-test-drive](https://github.com/PerryLink/dsh-test-drive)** |  |
| **[dsh-ticktick](https://github.com/PerryLink/dsh-ticktick)** | 🚫 रिटायर्ड (रेपो संग्रहीत) |
| **[dsh-translate](https://github.com/PerryLink/dsh-translate)** |  |
| **[dsh-warranty-calc](https://github.com/PerryLink/dsh-warranty-calc)** |  |
| **[dsh-budget](https://github.com/PerryLink/dsh-budget)** | 🧊 फ़्रोज़न — रेपो README देखें |
| **[dsh-claude-move](https://github.com/PerryLink/dsh-claude-move)** | 🧊 फ़्रोज़न — रेपो README देखें |
| **[dsh-defend](https://github.com/PerryLink/dsh-defend)** | 🧊 फ़्रोज़न — रेपो README देखें |
| **[dsh-draw](https://github.com/PerryLink/dsh-draw)** | 🧊 फ़्रोज़न — रेपो README देखें |
| **[dsh-reach](https://github.com/PerryLink/dsh-reach)** | 🧊 फ़्रोज़न — रेपो README देखें |
| **[dsh-background-agents](https://github.com/PerryLink/dsh-background-agents)** | 🚫 रिटायर्ड (रेपो संग्रहीत) |
| **[dsh-session-pin](https://github.com/PerryLink/dsh-session-pin)** | 🚫 रिटायर्ड (रेपो संग्रहीत) |
| **[dsh-team-rooms](https://github.com/PerryLink/dsh-team-rooms)** | 🚫 रिटायर्ड (रेपो संग्रहीत) |

</details>

## लाइसेंस

[LICENSE](LICENSE) (Apache License 2.0) © 2026 dsh-export-ctl-check contributors

<p align="center"><sub>Apache-2.0 · समुदाय प्लगइन, DeepSeek से संबद्ध नहीं।</sub></p>
