# billdogai.github.io

Source for **https://billdogai.github.io**: a hub for the BillDog codelabs (step-by-step paywall, subscription and A/B testing tutorials), the SDK install lines, and BillDog's open-source repositories.

The codelabs themselves live at **https://billdog.io/codelabs**.

## Regenerate

`index.html` is generated from the codelab list:

```bash
python3 _src/gen.py _src/codelabs.json index.html _src/template.html
```

`_src/codelabs.json` is exported from `src/data/codelabs` in the BillDog app. Re-export it when codelabs are added.
