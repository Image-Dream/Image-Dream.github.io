import os
import yaml

template = """
        <!-- ======================= -->
        <div class="col-xs-15">
            <img src="static/sdxl_rgba/{keyword}.png" alt="{keyword}" style="width: 80%">
        </div>
        <div class="row captioned_videos" id="res_{vid_id}" style="margin-top: 0px; margin-bottom: 0px ;">
            <video class="video lazy" loop playsinline autoplay muted style="width: 100%">
                <source data-src="static/compare_results_320/{keyword}.mp4" type="video/mp4"></source>
            </video>
            <p class="compare-caption">{description}</p>
        </div>
        """

with open("prompts.yaml", "r") as f:
    prompts = yaml.safe_load(f)
    keys = sorted(prompts.keys())

with open("test_template.html", "r") as f:
    html_template = f.read()
    
for i,k in enumerate(keys):
    print(k)

content = ""
page_idx = 0
prev_i = 0
page_size = 10
for i,k in enumerate(keys):
    description = prompts[k]
    current_video = template.format(vid_id=i, keyword=k, description=description)
    content += current_video
    
    first_page = page_idx - 1 < 0
    last_page = i + 1 >= len(keys)
    if i - prev_i + 1 >= page_size or last_page:
        link1 = f"test_{page_idx - 1}.html"
        link2 = f"test_{page_idx + 1}.html"
        active1 = "disabled" if first_page else ""
        active2 = "disabled" if last_page else ""
        html = html_template.replace("{{{content}}}", content).replace("{{{link1}}}", link1).replace("{{{link2}}}", link2)
        html = html.replace("{{{active1}}}", active1).replace("{{{active2}}}", active2)
        html = html.replace("{{{start_idx}}}", str(prev_i+1)).replace("{{{end_idx}}}", str(i+1)).replace("{{{total}}}", str(len(keys)))
        with open(f"test_{page_idx}.html", "w") as f:
            f.write(html)
        content = ""
        page_idx += 1
        prev_i = i + 1
