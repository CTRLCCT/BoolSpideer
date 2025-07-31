ZKEACMS is an open-source visual design developed using ASP.NET. NET MVC based on EasyFrameWork NET CMS

ZKEACMS has an arbitrary file upload vulnerability, allowing attackers to execute arbitrary commands by uploading carefully crafted theme files.

Vulnerable version:<=4.1

Official website: https://www.zkea.net/index

Source code: https://github.com/SeriaWei/ZKEACMS

V4.1 version source code: https://github.com/SeriaWei/ZKEACMS/releases/tag/v4.1

Environment setup: (specific connection:) https://www.zkea.net/zkeacms/document/startdev But it's a bit messy

1. The creation of the database is done in the database file of the source code, which contains SQL files. I use MySQL and a tool to create a "ZKEACMS" database, and then execute the SQL file.

And then C: \ wwwroot \ zkcms41 \ ZKEACMS-4.1 \ src \ ZKEACMS.WebHost folder to configure appsets.json

2.I built it using Visual Studio 2022 and first installed Visual Studio 2022 Net 6 SDK, Installed as follows:


<img width="692" height="307" alt="image" src="https://github.com/user-attachments/assets/96ca0dd9-60a5-4d9b-a36d-b296b4c628cb" />

Click on 'Open Project or Solution' and select the ZKEACMS.sln file from the downloaded source code, as follows:

<img width="692" height="214" alt="image" src="https://github.com/user-attachments/assets/b89a9ba9-d096-45ac-9d78-62927e4f8454" />

The first step is to click on "Generate" above and then click on "Generate Solution". The second step is to change the execution file above to "ZKEACMS. WebHost", then click the green execution button next to it and wait for a while. The browser will pop up http://localhost:5000/index , as follows:

<img width="692" height="150" alt="image" src="https://github.com/user-attachments/assets/f534dd62-ac04-4d47-b1c4-841794ed70dc" />

So the setup is successful, the backend/admin, and the account and password are all admin

Vulnerability description: 
The exploitation process is very simple, which is to construct a. theme file by yourself, and then upload this. theme file (called "joint. theme" here) in the "Basic Content" ->"Theme" ->"Install Theme" in the background. The system will then decompress this. theme file, so that the script we constructed to execute the command is also decompressed. Finally, click "View Site" to trigger "Command Execution".

Start reproducing as follows:

1. Construct. theme

You can obtain the. theme file by running rce. py

```shell
import gzip
from pathlib import Path
input_file = "rce.json"
output_file = "联合.theme"
text = Path(input_file).read_text(encoding="utf-8")
with gzip.open(output_file, "wb") as f_out:
    f_out.write(text.encode("utf-8"))
print(f"打包完成：{output_file}")
```

Explanation: 
This(. theme) is mainly generated from a (. json) file, which contains Filename (file name), FilePath (the location where some of the. theme files are saved after decompression), and Content (base64 encrypted, can be decrypted with tools). For example, in the following figure, there is an (Article. less) file, which will be finally decompressed to the~/themes/integrated/css/directory, with the content being a base64 file. Decoding is shown in the second figure

<img width="692" height="199" alt="image" src="https://github.com/user-attachments/assets/028fec61-1c75-4f87-b9f8-3bd2887a3aee" />

<img width="692" height="668" alt="image" src="https://github.com/user-attachments/assets/160ee69e-17c8-4bf3-82de-b711a3445392" />

That is to say, by modifying this (. json) file and adding the FileName as (Widget. Navigation. cshtml) (which must be named this) and the FilePath as~/themes/integrated/Views/Widget. (Navigation. cshtml) (which must be in this location), the content is as follows:

```shell
@using ZKEACMS.Common.Models
@using Microsoft.AspNetCore.Html
@model ZKEACMS.Common.ViewModels.NavigationWidgetViewModel
@{
     System.Diagnostics.Process.Start("calc.exe");
    if (!Model.Navigations.Any())
    {
        return;
    }
}
```

Then encrypt it using base64 and add it to the (. json) file as follows:

<img width="692" height="197" alt="image" src="https://github.com/user-attachments/assets/bb411e8b-19b2-4dd4-9d43-d3edf26c7b12" />

It is best to place it after the (_ViewImports. cshtml) file, as this will make the script more fake. Then run the (rce. py) script above to generate the (joint. theme) file
Then log in to the backend and click on "Basic Content" ->"Theme" ->"Install Theme", and upload the (joint. theme) file. After uploading, be sure to switch to the theme that was just uploaded.

<img width="693" height="373" alt="image" src="https://github.com/user-attachments/assets/430e22f0-5d2e-404c-9d70-4e7de3b0427b" />

Then the location of the script is saved in (C: \ wwwroot \ zkcms41 \ ZKEACMS-4.1 \ src \ ZKEACMS. WebHost \ wwwroot \ themes \ united \ Views).
Then click on 'View Site' above to trigger RCE, which will pop up the calculator

<img width="692" height="358" alt="image" src="https://github.com/user-attachments/assets/02358189-15a7-43a8-a182-590ba944b044" />

