from fastapi import UploadFile
import random
import os

MAX_FILE_SIZE = 1 * 1024 * 1024  # 1 MB


def assign_tasks(members: list[str], tasks: list[str]) -> dict[str, list[str]]:
    if not members or not tasks:
        return {member: [] for member in members}
    
    assignment = {member: [] for member in members}
    num_members = len(members)
    num_tasks = len(tasks)
    
    if num_tasks >= num_members:
        # Shuffle tasks to assign unique ones first
        task_list = list(tasks)
        random.shuffle(task_list) 
        
        # Assign one unique task to each member
        for i, member in enumerate(members):
            assignment[member].append(task_list[i])
        
        # Assign remaining tasks to random members
        for task in task_list[num_members:]:
            member = random.choice(members)
            assignment[member].append(task)
    else:
        # Shuffle members to assign unique tasks first
        member_list = list(members)
        random.shuffle(member_list)
        
        # Assign each task to a unique member
        for i, task in enumerate(tasks):
            member = member_list[i]
            assignment[member].append(task)
        
        # Assign random tasks to remaining members
        for member in member_list[num_tasks:]:
            task = random.choice(tasks)
            assignment[member].append(task)
    
    return assignment

def preprocess_lines(raw_data: str):
    lines = raw_data.splitlines()
    clean_lines = [line.strip() for line in lines if line.strip()]
    return clean_lines

async def check_file_size(upload_file: UploadFile):
    contents = await upload_file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise ValueError("File too large.")
    await upload_file.seek(0)  # reset cursor after reading
    return contents


if __name__ == "__main__":
    members = [
            "Alice",    
            "Bob",       
            "Chloe",      
            "David",     
            "Emma",      
            "Frank",
            "Grace",      
            "Hassan"    
        ]

    tasks = [
            "Rotate all AWS access keys older than 90 days",
            "Update Terraform to latest 1.x version in all modules",
            "Implement GitHub branch protection rules for main branch",
            "Reduce EKS cluster cost by rightsizing nodes",
            "Migrate remaining services from Jenkins to GitHub Actions",
            "Run Trivy scan on all Docker images and fix critical CVEs",
            "Add chaos engineering experiment (pod termination) in staging",
            "Document on-call rotation handover process",
        ]
    
    print(assign_tasks(tasks, members))