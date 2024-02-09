ifeq ($(OS), Windows_NT)
init:
	@pip install -r requirements.txt

user:
	@sanic main --debug --reload

note:
	@uvicorn main:note_app --port 8001 --reload

label:
	@uvicorn main:label_app --port 8002 --reload
endif