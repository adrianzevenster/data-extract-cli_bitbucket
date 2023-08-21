setup:
	python3 -m venv .venv --copies
	.venv/bin/python -m pip install pipenv
	.venv/bin/python -m pipenv install --dev

test:
	.venv/bin/behave

package:
	.venv/bin/pyinstaller -y --add-data ".venv/lib/python3.8/site-packages/pyfiglet:./pyfiglet" \
	  --add-data "templates:./templates" \
    --paths .venv/lib/python3.8/site-packages/ src/main.py
	.venv/bin/pyinstaller --add-data ".venv/lib/python3.8/site-packages/pyfiglet:./pyfiglet" \
    --onefile --paths .venv/lib/python3.8/site-packages/ scripts/install.py
	cp src/.env.example dist/.env.example
	cp docs/dist-instructions.md dist/README.md
	cp src/extract-request.json.example dist/extract-request.json.example
	chmod +X dist/install dist/main
	zip -r -9 dist.zip dist
