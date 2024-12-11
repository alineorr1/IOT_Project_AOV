# footer.py
import dash
from dash import html, dcc

#%%

footer1 = html.Footer(
        html.Div(
            [
                html.Hr(),
                dcc.Markdown(
                    """
                **Alexa-Dash**  
                """
                ),
                html.P(
                    [
                        html.Img(src=dash.get_asset_url("agbc32.jpg")),
                        html.Span("   "),
                        html.A("GitHub Repository", href="https://github.com/KaxaNuk-Community/C_AGBC-Alexa", target="_blank"),
                    ]
                ),
            ],
            style={"text-align": "center"},
            className="p-3",
        ),
    )