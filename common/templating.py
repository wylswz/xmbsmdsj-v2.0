from jinja2 import Template


def paragraph(text, margin):
    if margin not in {0,1,2,3,4,5}:
        raise ValueError("Margin must be between 0 and 5")
    return '<p class=\".mb-{margin}\"> {text} </p>'.format(
        margin=margin,
        text=text,
    )

def multiline_html_paragraph(text: str, margin:int=1) -> str:
    ps = text.split('\n')
    return "\n".join(
        paragraph(p, margin) for p in ps
    )

