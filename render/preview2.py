import asyncio, json, glob, os
from playwright.async_api import async_playwright
from PIL import Image
JS = open("bundle.js").read()
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width":1280,"height":720})
        await pg.set_content("<html><body></body></html>"); await pg.add_script_tag(content=JS)
        os.makedirs(os.environ.get("PV","../prev2")+"", exist_ok=True)
        for f in sorted(glob.glob(os.environ.get("SC","../scenes2")+"/*.excalidraw")):
            els = json.load(open(f))["elements"]
            anchor = {**els[0], "id":"anchor","type":"rectangle","x":0,"y":0,"width":1280,"height":720,"strokeColor":"transparent","backgroundColor":"transparent","groupIds":[]}
            svg = await pg.evaluate("""async (els)=>{const s=await window.exportToSvg({data:{elements:els,appState:{exportBackground:true,viewBackgroundColor:'#fff'},files:{}},config:{padding:0}});return s.outerHTML}""", [anchor]+els)
            q = await b.new_page(viewport={"width":1280,"height":720})
            await q.set_content("<html><body style='margin:0'>"+svg+"</body></html>")
            await q.screenshot(path=os.environ.get("PV","../prev2")+"/"+os.path.basename(f).replace(".excalidraw",".png")); await q.close()
        await b.close()
asyncio.run(main())
fs = sorted(glob.glob(os.environ.get("PV","../prev2")+"/[0-9]*.png"))
for k in range(0, len(fs), 6):
    ims = [Image.open(f).convert("RGB").resize((640,360)) for f in fs[k:k+6]]
    s = Image.new("RGB", (1290, 1100), "#888")
    for n, i in enumerate(ims): s.paste(i, ((n%2)*650, (n//2)*370))
    s.save(os.environ.get("PV","../prev2")+f"/sheet{k//6+1}.png")
