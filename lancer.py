import streamlit.web.cli as stcli
import sys
if __name__ == "__main__":
    sys.argv = ["streamlit", "run", "dashboard_phone.py"]
    stcli.main()