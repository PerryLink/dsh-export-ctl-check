# dsh-export-ctl-check — निर्यात-नियंत्रण मद रजिस्टर और लाइसेंस की बंद-कड़ी की जाँच

[![DSH Market](https://raw.githubusercontent.com/2BingLing/dsh-market/master/assets/readme/badge-listed-en.svg)](https://dsh.market/)

`dsh-export-ctl-check` एक निर्यात-नियंत्रण मद रजिस्टर पढ़ता है — निर्यातक हेडर और हर मद की एक पंक्ति — और उसी रजिस्टर की पूर्णता तथा बंद-कड़ी (closure) की जाँच करता है, मदों के बारे में कोई निर्णय नहीं: क्या हर मद 是否受控 कॉलम में लिखती है कि वह नियंत्रित है या नहीं, क्या नियंत्रित बताई गई मद में 出口许可证号 दर्ज है, क्या दर्ज लाइसेंस क्रमांक के साथ जारी करने की तिथि भी है, क्या अंतिम उपयोग या अंतिम उपयोगकर्ता में से कम से कम एक दर्ज है, क्या अंतिम गंतव्य दर्ज है, क्या एक ही रजिस्टर में लाइसेंस क्रमांक दोहराया गया है, क्या नियंत्रण श्रेणी संस्था के अपने 管制类别 मानों में से है, और क्या मद-नाम कॉलम में 【】, XXX, 待填, TBD या 示例 जैसा कोई प्लेसहोल्डर शेष है।

## आउटपुट कैसा दिखता है

![Terminal demo of dsh-export-ctl-check: real output over its EC-001 fixture](https://raw.githubusercontent.com/PerryLink/dsh-export-ctl-check/main/docs/assets/dsh-export-ctl-check-demo.png)

इस प्लगइन का अपने ही `EC-001` टेस्ट फ़िक्स्चर पर वास्तविक आउटपुट — कोई नकली चित्र नहीं। नियम-पैक उद्धरण नहीं गढ़ता, इसलिए हर निष्कर्ष लागू किए गए खंड का नाम और यह भी बताता है कि उसका मूल पाठ इस बार प्राप्त नहीं हुआ।

## यह किन सवालों का जवाब देता है

| आपका सवाल | इसका जवाब |
|---|---|
| नियंत्रित बताई गई मद में लाइसेंस क्रमांक न हो तो क्या यह दर्ज होता है? | `EC-002` यह कमी दर्ज करता है: जिस पंक्ति का 是否受控 मान उन मानों में है जिन्हें यह नियम नियंत्रित मानता है — डिफ़ॉल्ट रूप से `是`, `Y`, `yes`, `true`, `受控`, `√` — उसके लिए 出口许可证号 ज़रूरी है। यह केवल देखता है कि क्रमांक भरा है; यह नहीं आँकता कि लाइसेंस असली है, अब भी वैध है, या उस मद और उस गंतव्य को कवर करता है। यदि आपका रजिस्टर «नियंत्रित» के लिए कोई और शब्द लिखता है तो उसे इस नियम के शर्त-मानों में जोड़ें, वरना वह पंक्ति अनियंत्रित गिनी जाएगी और नियम चुप रहेगा — इस प्लगइन में कोई नियंत्रण-सूची नहीं है जो आपकी ओर से यह तय करे। |
| मद में यह लिखा है कि वह नियंत्रित है या नहीं, पर 最终用途 और 最终用户 दोनों कॉलम खाली हैं। क्या यह पकड़ में आता है? | `EC-004` उस पंक्ति को दर्ज करता है: वह इन दोनों में से कम से कम एक कॉलम भरा होने की अपेक्षा करता है। एक भर जाना पर्याप्त है, और नियम यह नहीं आँकता कि बताया गया उपयोग या उपयोगकर्ता सच है, या मामला कानून द्वारा निषिद्ध या प्रतिबंधित श्रेणी का है। |
| लाइसेंस क्रमांक दर्ज है, पर जारी करने की तिथि का कॉलम खाली है। क्या यह कोई खामी है? | `EC-003` उसे ज़रूरी मानता है। शर्त लाइसेंस क्रमांक है: जिस पंक्ति में क्रमांक ही नहीं, उससे तिथि नहीं माँगी जाती। नियम लाइसेंस की वैधता-अवधि नहीं जाँचता और जारी करने की तिथि की तुलना निर्यात की तिथि से नहीं करता — वह केवल यह स्थापित करता है कि तिथि दर्ज है, यह नहीं कि वह पहले की है। |
| एक ही लाइसेंस क्रमांक कई पंक्तियों में आया है। जाँच क्या कहती है? | `EC-006` उस क्रमांक को रजिस्टर के भीतर दोहराया गया बताकर दर्ज करता है। वह यह अंतर नहीं कर पाता कि एक लाइसेंस कई मदों को कवर करता है — जो रजिस्टर रखने का सामान्य तरीका है — या क्रमांक भूल से कॉपी हुआ है, इसलिए परिणाम की पुष्टि किसी व्यक्ति को करनी होती है; नियम किसी क्रमांक को बदलता नहीं और यह भी नहीं बताता कि एक लाइसेंस कितनी पंक्तियों में आ सकता है। यदि आपका रजिस्टर जान-बूझकर «एक लाइसेंस, कई मदें» के रूप में है तो उस लाइसेंस की पंक्तियों पर क्रमांक डालकर अलग दिखाएँ, या नियम बंद कर दें। |
| किसी पंक्ति में 最终目的地 ही नहीं है। | `EC-005` उसे दर्ज करता है, क्योंकि हर मद में गंतव्य होना चाहिए। यह देखता है कि कॉलम भरा है, यह नहीं कि गंतव्य अनुमत है: कोई देश या क्षेत्र प्रतिबंधित है या नहीं, यह सक्षम प्राधिकरण की प्रकाशित सूचियों से पढ़ा जाता है, और इस प्लगइन में अपनी कोई देश-सूची नहीं है। |
| मद-नाम कॉलम में अब भी `【示例】` या `XXX` लिखा है — इसे खामी माना जाता है या असली नाम? | जब नाम में वे शब्द मिलते हैं जिन्हें नियम खोजता है, तब `EC-008` उस पंक्ति को दर्ज करता है — ये शब्द हैं `【`, `】`, `{{`, `}}`, `XXX`, `xxx`, `待填`, `待补充`, `TBD`, `todo` और `示例`। यह शब्द-सूची आपके अपने टेम्पलेट के अनुसार है और बदली जा सकती है। नियम इन शब्दों को केवल उसी एक कॉलम में देखता है: वह नाम के तथ्यात्मक रूप से सही होने का निर्णय कभी नहीं करता। |

## यह किन मानकों पर आधारित है

| दस्तावेज़ | संख्यांक | इन्हें उद्धृत करने वाले नियम |
|---|---|---|
| 《中华人民共和国出口管制法》 | 2020 年 10 月 17 日第十三届全国人大常委会第二十二次会议通过，主席令第五十八号公布，自 2020 年 12 月 1 日起施行 | EC-001, EC-002, EC-003, EC-004, EC-005, EC-006, EC-008 |
| 《中华人民共和国出口管制法》 | 现行版本本次未核实 | EC-007 |

**Boundary:** this plugin checks an **出口管制物项台账** for the closed loop a register can be held to — that
each item states whether it is controlled, that a controlled item carries a licence number, that a licence
carries an issue date, that the end use or end user is recorded, that a destination is recorded, that licence
numbers do not repeat, that the control category comes from your vocabulary, and that no placeholder survives.
It does **not** decide whether an item is controlled, whether a licence is required, or whether an export would
breach the rules.

> ### ⚠️ What this plugin deliberately cannot do
>
> **It does not contain the control list, and it does not try to map a commodity code or a technical parameter
> onto a list entry.** Because of that it **cannot find the most serious defect of all: an item that should
> have been declared controlled and was not.** Whether an item is controlled is the exporter's own
> determination under the law, and confirming it means checking the published list. This limit is stated in
> the pack's header, in each rule's note, and in the troubleshooting section below — it is the single most
> important thing to know about this plugin.
>
> The 是否受控 column is therefore the register's own declaration. Everything here checks what happens *after*
> that declaration: is a licence recorded, is it dated, is the destination and end use stated, does the
> register hold together. **It never checks whether the declaration was right.**
>
> **Every `excerpt` in the rule pack says, in so many words, that the clause text was not obtained.** The
> regime lives in 《中华人民共和国出口管制法》, the dual-use export licensing measures, and the published
> control list. The verification pass could not retrieve verbatim clause text, so the pack states the gap in
> the `excerpt` field itself and keeps every rule at `warn` or `info`. **When the texts are in hand, replace
> each `excerpt` with the real clause and raise `kind` to `direct`.**

## Compatibility

| सतह | स्थिति |
|---|---|
| Harness | peer रेंज `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` — `0.2.0-rc.2` और `0.2.1-alpha.1` दोनों को स्वीकार करने के लिए सत्यापित। **`engines.dsh` जानबूझकर घोषित नहीं**: इसका कोई पाठक नहीं और यह किसी होस्ट को अस्वीकार नहीं कर सकता |
| Node | `^22.19.0 || >=24.0.0` |
| प्लेटफ़ॉर्म | सभी (शुद्ध ESM; कोई नेटिव कोड नहीं, कोई नेटवर्क नहीं, कोई मॉडल कॉल नहीं) |
| टूल मोड | `native`, `ptc` और `both` में काम करता है; पूरे फ़ोल्डर के लिए `ptc` चुनें |

## What it does

नियम-सूची, फ़ील्ड और विस्तृत व्यवहार [README.md](README.md#what-it-does) (अंग्रेज़ी मुख्य संस्करण) में हैं। यह प्लगइन केवल उद्धृत धाराओं के सामने शाब्दिक अंतर सूचीबद्ध करता है और हर न चल पाई जाँच को `skipped` में बताता है।

## Install

```sh
dsh plugin --profile <name> add dsh-export-ctl-check
dsh --profile <name> --dump-config | grep 'dsh-export-ctl-check'
```

## Configuration

सभी समायोज्य पैरामीटर `src/config.ts` की Schemastery स्कीमा में हैं, इसलिए कोड बदले बिना `cordis.yml` से बदले जा सकते हैं; प्रति-नियम सीमाएँ `rules/` के नियम-पैक में हैं।

| कुंजी | प्रकार | डिफ़ॉल्ट | विवरण |
|---|---|---|---|
| `rulesFile` | string | `rules/export-ctl-check.yaml` | नियम-पैक का पथ, पैकेज रूट के सापेक्ष |
| `disabledRules` | string[] | `[]` | बंद करने वाले नियम id; प्रत्येक `skipped` में दिखता है |
| `onlyRules` | string[] | `[]` | केवल ये नियम चलाएँ; खाली होने पर सभी नियम चलते हैं |
| `skipNotes` | string | `""` | हर `skipped` कारण के आगे जोड़ी जाने वाली टिप्पणी |
| `timeoutMs` | number | `120000` | उपकरण का सहकारी समय-सीमा बजट |

## Material format

JSON या YAML स्वीकार्य है। पूरा फ़ील्ड उदाहरण [README.md](README.md#material-format) (अंग्रेज़ी मुख्य संस्करण) में है। पढ़ने की परत में फ़ील्ड वैकल्पिक हैं और जाँच इंजन उन्हें सत्यापित करता है, इसलिए आंशिक निर्यात पर क्रैश के बजाय "अनुपस्थित" श्रेणी के निष्कर्ष मिलते हैं।

## Rule sources

नियम-डेटा कोड से अलग है: प्रत्येक नियम में दस्तावेज़, संख्या, स्रोत की अपनी क्रमांकन-प्रणाली के अनुसार धारा, शब्दशः उद्धरण और स्रोत URL होता है। लोडर लागू करता है कि उद्धरण कम से कम आठ अक्षरों का वास्तविक उद्धरण हो, और जिस जाँच का आधार केवल सामान्य सिद्धांत (`kind: derived-from-principle`, अधिकतम `warn`) या स्थानीय नीति (`kind: institutional-configuration`, अधिकतम `info`) हो, उसे कभी `error` घोषित न किया जाए।

सत्यापित सीमाएँ और जान-बूझकर **न** कहे गए निष्कर्ष [README.md](README.md#rule-sources) (अंग्रेज़ी मुख्य संस्करण) और `rules/evidence/` में हैं।

## Troubleshooting

- **प्लगइन इंस्टॉल हो गया पर टूल दिखता नहीं**: जाँचें कि `main` `lib/index.mjs` पर जाता है और `pnpm run build` ने उसे बनाया है।
- **`dsh plugin add` असंगत बताकर मना करता है**: peer range `0.1.x` और `0.2.x` दोनों को कवर करती है; बाहर होने पर स्पष्ट छूट दें: `dsh plugin --profile <name> allow-version <pkg@ver> --dsh-version <runtime> --accept-risk`।
- **कोई नियम नहीं चला**: `skipped` सरणी देखें।
- **`check` में `manifest-peers` विफल दिखता है**: यह `dsh-plugin-dev` की ज्ञात अपस्ट्रीम समस्या है; रनटाइम इंस्टॉल के समय अनुकूलता लागू करता है।
- **समय खिसका हुआ लगता है**: सारी गणना दिए गए स्ट्रिंग पर वॉल-क्लॉक है।

## Development

```sh
pnpm install
pnpm run typecheck
pnpm test
pnpm run build
node ../scripts/sync-shared.mjs dsh-export-ctl-check
```

अंतिम कमांड `../_shared` का साझा किट `src/shared/` में कॉपी करता है; हर साझा बदलाव के बाद इसे दोबारा चलाएँ।

## License

[Apache License 2.0](LICENSE) © 2026 dsh-export-ctl-check contributors.
