from typing import Any, Dict, List
import json

class NotebookAdapter:
    def __init__(self, notebook_path: str):
        self.notebook_path = notebook_path

    def load_notebook(self) -> Dict[str, Any]:
        with open(self.notebook_path, 'r') as f:
            return json.load(f)

    def get_cells(self) -> List[Dict[str, Any]]:
        notebook_content = self.load_notebook()
        return notebook_content.get('cells', [])

    def get_code_cells(self) -> List[Dict[str, Any]]:
        cells = self.get_cells()
        return [cell for cell in cells if cell['cell_type'] == 'code']

    def get_markdown_cells(self) -> List[Dict[str, Any]]:
        cells = self.get_cells()
        return [cell for cell in cells if cell['cell_type'] == 'markdown']

    def execute_code_cell(self, cell: Dict[str, Any]) -> Any:
        # Placeholder for executing the code cell
        # This function should interface with the execution environment
        code = ''.join(cell['source'])
        # Execute the code and return the result
        return eval(code)  # Caution: eval can be dangerous if not controlled

    def run_all_code_cells(self) -> List[Any]:
        code_cells = self.get_code_cells()
        results = []
        for cell in code_cells:
            result = self.execute_code_cell(cell)
            results.append(result)
        return results

# Example usage:
# adapter = NotebookAdapter('path/to/notebook.ipynb')
# results = adapter.run_all_code_cells()