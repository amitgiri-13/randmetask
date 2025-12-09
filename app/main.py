from fastapi import FastAPI, UploadFile, File, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import csv

from .utils import assign_tasks, preprocess_lines, check_file_size

app = FastAPI()

templates = Jinja2Templates(directory="app/templates")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def upload_page(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})


@app.post("/assign", response_class=HTMLResponse)
async def assign_tasks_route(
    request: Request,
    members_file: UploadFile = File(...),
    tasks_file: UploadFile = File(...)
    ):

    try:
       # Read and check file size
        members_data = await check_file_size(members_file)
        tasks_data = await check_file_size(tasks_file)

        # Decode and preprocess lines
        members = preprocess_lines(members_data.decode())
        tasks = preprocess_lines(tasks_data.decode())

        if not members or not tasks:
            raise ValueError("Uploaded files must contain at least one valid line.")

        # Assign randomly
        assignments = assign_tasks(members, tasks)

        # Save to CSV (optional)
        output_file = f"app/static/assignments.csv"
        import csv
        with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Task", "Assigned To"])
            for task, assigned_members in assignments.items():
                writer.writerow([task, ", ".join(assigned_members)])

        # Render result
        return templates.TemplateResponse(
            "result.html",
            {"request": request, "assignments": assignments, "download_link": "/static/assignments.csv"}
        )

    except ValueError as e:
        return templates.TemplateResponse(
        "error.html",
        {"request": request, "error_message": str(e)},
        status_code=400
    )
