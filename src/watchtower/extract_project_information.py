import argparse
from datetime import date
import os
import pandas as pd


parser = argparse.ArgumentParser()
parser.add_argument("filename",
                    help=("CSV file containing the project "
                          "registration information."))
parser.add_argument("--outdir", "-o", default="build")
args = parser.parse_args()

columns = ["timestamp", "username", "name", "contact", "github_org",
           "description", "language", "url", "goal", "help",
           "has_github_project",
           "github_project_url"]
information = pd.read_csv(args.filename, header=None, skiprows=1,
                          names=columns)

header = (
    "Title: {project_name}\n"
    "Date: {registration_date}\n"
    "Modified: {now}\n"
    "Tags: projects, docathon\n"
    "Category: info\n"
    "Slug: projects/{project_name}\n"
    "Authors: watchtower\n"
    "Summary: {project_name}\n"
    "Status: hidden\n"
    "\n"
      )

try:
    os.makedirs(args.outdir)
except OSError:
    pass

print('Creating pages for {} projects'.format(len(information)))
projects = {}
for ix, project in information.iterrows():

    project_name = project['name']
    project_url = project['url']
    project_user = project['github_org'].split('/')[-2:][0]
    project_description = project['description']
    project_name_lc = project_name.lower().replace(" ", "_")
    filename = os.path.join(args.outdir, project_name_lc + ".md")
    header_formatted = header.format(
        project_name=project_name,
        registration_date=project['timestamp'],
        now=date.today().strftime("%Y-%m-%d"),
        project_description=project_description)

    projects[project_name] = os.path.join(args.outdir,
                                          project_name_lc + ".html")

    # Write the content page
    with open(filename, "w") as f:
        f.write(header_formatted)
        if isinstance(project_url, str):
            f.write(
                "* **Documentation** [{project_url}]({project_url})\n".format(
                    project_url=project_url))
        f.write(
            "* **Description** {project_description}\n".format(
                project_description=project_description))
    
    # Compile list of which projects we've pulled
    open_as = 'w' if ix == 0 else 'a'
    with open('.downloaded_projects', open_as) as ff:
        ff.writelines('{},{}\n'.format(project_user, project_name))

# Now create one page for all the projects
header_index = (
    "Title: Projects\n"
    "Date: 2017-02-18\n"
    "Modified: {now}\n"
    "Tags: projects, docathon\n"
    "Category: info\n"
    "Slug: projects/projects\n"
    "Authors: watchtower\n"
    "Summary: List of projects\n"
    "\n")

filename = os.path.join(args.outdir, "projects.md")
header_formatted = header_index.format(now=date.today().strftime("%Y-%m-%d"))
project_template = "* [{project_name}]({project_url})\n"
with open(filename, "w") as f:
    f.write(header_formatted)

    for project, url in projects.items():
        f.write(project_template.format(project_name=project,
                project_url=url))
