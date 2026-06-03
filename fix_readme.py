f = open('README.md', 'r', encoding='utf-8')
content = f.read()
f.close()

bad = '[

![Live Dashboard](https://img.shields.io/badge/Live%20Dashboard-Click%20Here-brightgreen)

\n\n](https://environmental-data-pipeline-2dnkog5rys5suebnkpqyzv.streamlit.app)-'
good = '[

![Live Dashboard](https://img.shields.io/badge/Live%20Dashboard-Click%20Here-brightgreen)

](https://environmental-data-pipeline-2dnkog5rys5suebnkpqyzv.streamlit.app)'

content = content.replace(bad, good)

f = open('README.md', 'w', encoding='utf-8')
f.write(content)
f.close()
print('Done')