import asyncio, json, os, sys
sys.path.insert(0, "..")
from sprites import sprite_defs
from playwright.async_api import async_playwright
K = 1653 / 1280; M = 14
JS = open("bundle.js").read()
async def main():
    D = sprite_defs(); os.makedirs("sprites", exist_ok=True); meta = {}
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page()
        await pg.set_content("<html><body></body></html>"); await pg.add_script_tag(content=JS)
        shot = await b.new_page()
        for name, (els, (w, h)) in D.items():
            anchor = {**els[0], "id": "anc", "type": "rectangle", "x": -M, "y": -M, "width": w + 2 * M, "height": h + 2 * M, "angle": 0,
                      "strokeColor": "transparent", "backgroundColor": "transparent", "opacity": 0, "groupIds": [], "boundElements": None}
            pw, ph = round((w + 2 * M) * K), round((h + 2 * M) * K)
            svg = await pg.evaluate("""async ([els,pw,ph])=>{const s=await window.exportToSvg({data:{elements:els,
                appState:{exportBackground:false},files:{}},config:{padding:0}});s.setAttribute('width',pw);s.setAttribute('height',ph);return s.outerHTML}""", [[anchor] + els, pw, ph])
            await shot.set_viewport_size({"width": pw, "height": ph})
            await shot.set_content("<html><body style='margin:0;background:transparent'>" + svg + "</body></html>")
            await shot.screenshot(path=f"sprites/{name}.png", omit_background=True)
            meta[name] = {"w": w, "h": h, "m": M}
        await b.close()
    json.dump(meta, open("sprites/meta.json", "w"))
    print(len(meta), "sprites")
asyncio.run(main())
