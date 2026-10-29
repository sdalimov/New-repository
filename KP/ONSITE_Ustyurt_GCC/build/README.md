# Сборка КП ONSITE → Устюртский ГХК

1. Впишите цены (`price`), торговые наименования и номер КП (`KP_NO`) в `kp_data.py`.
2. Из папки `KP/ONSITE_Ustyurt_GCC` выполните:

```bash
python3 -I build/build_xlsx.py build/RFQ_original.xlsx RFQ_Chemicals_ONSITE.xlsx
python3 -I build/build_docx.py build/onsite_logo.jpg KP_ONSITE_Ustyurt_GCC.docx
```

Чтобы поставить печать и подпись, добавьте к команде для `.docx` параметр `--stamp <файл печати>`.
