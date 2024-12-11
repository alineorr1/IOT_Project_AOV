# navigation.py
import dash_bootstrap_components as dbc
import dash_html_components as html

#%%

navbar = dbc.Navbar(
    [
        dbc.Row(
            [
                dbc.Col(html.Img(src="assets/iot.png", 
                                 height="32px", style={"marginLeft": "8px"}), 
                        width=2),  # Added marginLeft style directly
            ],
            align="center",
            justify="start"
        ),
        dbc.NavbarToggler(id="navbar-toggler", style={"color": "red"}),
        dbc.Collapse(
            dbc.Nav(
                [
                    dbc.NavItem(dbc.NavLink("Oura Ring", href="/day-analysis", style={"color": "black", "fontWeight": "bold", "fontSize": "16px"})),  # Adjusted font-weight and font-size
                    dbc.NavItem(dbc.NavLink("Oura Ring Historical Analysis", href="/historical-page", style={"color": "black", "fontWeight": "bold", "fontSize": "16px"})),  # Adjusted font-weight and font-size
                    dbc.NavItem(dbc.NavLink("HeartRate Analysis", href="/heartrate-page", style={"color": "black", "fontWeight": "bold", "fontSize": "16px"})),  # Adjusted font-weight and font-size
                    dbc.NavItem(dbc.NavLink("Weather Quality Analysis", href="/weather-page", style={"color": "black", "fontWeight": "bold", "fontSize": "16px"})),  # Adjusted font-weight and font-size
                    dbc.DropdownMenu(
                        children=[
                            dbc.DropdownMenuItem("Oura Developer Forum", href="https://cloud.ouraring.com/v2/docs#section/Overview", style={"color": "blue"}),
                        ],
                        nav=True,
                        in_navbar=True,
                        label="More",
                        style={"color": "red"},
                    ),
                ],
                navbar=True,
            ),
            id="navbar-collapse",
            navbar=True,
        ),
    ],
    color="light",
    dark=False,
)
