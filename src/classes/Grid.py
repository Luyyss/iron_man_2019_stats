import streamlit as st
from src.classes.Cell import Cell
from typing import Optional

class Grid:
    """A (CSS) Grid"""

    def __init__(
        self,
        template_columns="1 1 1",
        gap="10px",
        background_color="#FFF",
        color="#000"
    ):
        self.template_columns = template_columns
        self.gap = gap
        self.background_color = background_color
        self.color = color
        self.cells: List[Cell] = []

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        st.markdown(self._get_grid_style(), unsafe_allow_html=True)
        st.markdown(self._get_cells_style(), unsafe_allow_html=True)
        st.markdown(self._get_cells_html(), unsafe_allow_html=True)

    def _get_grid_style(self):
        return f"""
        <style>
            .wrapper {{
                display: grid;
                grid-template-columns: {self.template_columns};
                grid-gap: {self.gap};
            }}
            .box {{
                background-color: {self.background_color};
                color: {self.color};
                border-radius: 5px;
                padding: 20px;
                font-size: 150%;
            }}
            table {{
                color: {self.color}
            }}
        </style>
        """

    def _get_cells_style(self):
        return (
            "<style>"
            + "\n".join([cell._to_style() for cell in self.cells])
            + "</style>"
        )

    def _get_cells_html(self):
        return (
            '<div class="wrapper">'
            + "\n".join([cell._to_html() for cell in self.cells])
            + "</div>"
        )

    def cell(
        self,
        class_: str = None,
        grid_column_start: Optional[int] = None,
        grid_column_end: Optional[int] = None,
        grid_row_start: Optional[int] = None,
        grid_row_end: Optional[int] = None,
    ):

        cell = Cell(
            class_=class_,
            grid_column_start=grid_column_start,
            grid_column_end=grid_column_end,
            grid_row_start=grid_row_start,
            grid_row_end=grid_row_end,
        )
        self.cells.append(cell)
        return cell
