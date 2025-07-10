import os
import sys
import io
from io import StringIO

import traceback
import base64
import matplotlib.pyplot as plt

class PythonREPL:
    def run(self, code: str) -> str:
        """
        Execute Python code in a REPL (Read-Eval-Print Loop) environment.

        Args:
            code: The Python code to be executed.

        Returns:
            The output of the executed code or an error message if an exception occurs.
        """
        old_stdout = sys.stdout
        redirected_output = sys.stdout = StringIO()
        try:
            exec(code, globals())
            sys.stdout = old_stdout

            return redirected_output.getvalue()
        except Exception as e:
            sys.stdout = old_stdout
            return f"Error: {str(e)}\n {traceback.format_exc()}"

    def data_visualization(self, code: str) -> str:
        """
        Executes the provided Python code to generate a plot, saves the plot as a PNG image, 
        encodes it in Base64 format, and returns it as a data URL.

        This function is designed to execute user-provided Python code that generates a plot using libraries like Matplotlib. 
        The generated plot is saved as a PNG image, encoded into Base64 format, and returned as a data URL for easy embedding 
        in web pages or other applications.

        Args:
            code: The Python code to be executed. The code is expected to generate a plot using a plotting library such as Matplotlib.
                Ensure that the code does not contain any harmful or malicious operations, as it will be executed in the current environment.

        Returns:
            If successful, the function returns a Base64 encoded string representing the generated plot image in PNG format, 
            prefixed with "data:image/png;base64," for use as a data URL.
            If the provided code fails to execute or the image encoding process fails, an error message is returned instead.

        Example Usage:
            The following example demonstrates how to use this function to generate a simple line plot:

            ```python

            # Define the Python code to generate a plot
            code = '''
            import matplotlib.pyplot as plt
            plt.figure(figsize=(6, 4))
            plt.plot([1, 2, 3, 4], [10, 20, 25, 30], marker='o')
            plt.title("Sample Plot")
            plt.xlabel("X-axis")
            plt.ylabel("Y-axis")
            '''

            # Call the function
            result = data_visualization(code) #  a Base64-encoded data URL of the plot image

            ```

        Notes:
            - Ensure that the provided code generates a valid plot before calling this function.
            - The function uses `io.BytesIO` to handle binary image data, as plots are saved in binary format (PNG).
            - If the code execution fails (e.g., due to syntax errors or missing dependencies), an error message is returned.
            - Be cautious when executing untrusted code, as it may introduce security risks.

        Raises:
            Exception: Any exceptions raised during the execution of the provided code or the image encoding process are caught 
                    and returned as part of the error message.
        """
        try:
            self.repl.run(code)
            buf=io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            img_str=base64.b64encode(buf.getvalue()).decode()
            buf.close()
            return f"data:image/png;base64,{img_str}"
        except Exception as e:
            return f"Error: {str(e)}"
