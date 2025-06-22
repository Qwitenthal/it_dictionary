import pandas as pd

# Завантаження CSV-файлу
file_path = "slovnyk.csv"
df = pd.read_csv(file_path)

df["Сфера вживання"] = df["Сфера вживання"].replace("менеджмент", "загальне")

# Сортування з ігноруванням неалфавітних символів
def normalize_sort_key(word):
    word = str(word).strip().lower()
    while word and not word[0].isalpha():
        word = word[1:]
    return word

df["sort_key"] = df["Слово"].apply(normalize_sort_key)
df_sorted = df.sort_values(by="sort_key").drop(columns=["sort_key"])

# Унікальні значення для фільтрів
unique_domains = sorted(df_sorted["Сфера вживання"].dropna().unique())
unique_pos = sorted(df_sorted["Частина мови"].dropna().unique())

# Початок HTML
html_content = """
<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <title>Словник веброзробників</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; margin: 40px; background-color: #eef1f5; }
        h1 { color: #2c3e50; }
        .filters { margin-bottom: 20px; }
        input, select, button {
            padding: 10px; margin-right: 10px; border-radius: 6px;
            border: 1px solid #ccc; font-size: 16px;
        }
        button {
            background-color: #e74c3c; color: white; border: none; cursor: pointer;
        }
        table {
            width: 100%; border-collapse: collapse; background-color: #fff;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        th, td { padding: 12px; text-align: left; }
        th {
            background-color: #4CAF50; color: white;
            position: sticky; top: 0; z-index: 2;
        }
        tr:nth-child(even) { background-color: #f7f9fc; }
        tr:hover { background-color: #e0f7e9; }
        #noResults { color: #e74c3c; font-weight: bold; display: none; margin-top: 10px; }
        #resultCount { margin-top: 10px; font-weight: bold; }
    </style>
</head>
<body>
    <h1>Словник сленгу веброзробників</h1>

    <div class="filters">
        <input type="text" id="searchInput" onkeyup="filterTable()" list="suggestions" placeholder="🔍 Пошук...">
        <datalist id="suggestions">
"""

# Автозаповнення
for _, row in df_sorted.iterrows():
    html_content += f'<option value="{row["Слово"]}">\n'

html_content += """
        </datalist>

        <select id="domainSelect" onchange="filterTable()">
            <option value="">🌐 Усі сфери</option>
"""

for domain in unique_domains:
    html_content += f'<option value="{domain}">{domain}</option>\n'

html_content += """
        </select>

        <select id="posSelect" onchange="filterTable()">
            <option value="">🧠 Усі частини мови</option>
"""

for pos in unique_pos:
    html_content += f'<option value="{pos}">{pos}</option>\n'

html_content += """
        </select>

        <button onclick="clearFilters()">Очистити фільтри</button>
    </div>

    <div id="resultCount"></div>
    <div id="noResults">Немає результатів за запитом 😕</div>

    <table id="dictionaryTable">
        <thead>
        <tr>
            <th>Слово</th>
            <th>Частина мови</th>
            <th>Значення</th>
            <th>Приклад</th>
            <th>Сфера</th>
            <th>Іншомовний відповідник</th>
            <th>Літературний відповідник</th>
        </tr>
        </thead>
        <tbody>
"""

# Заповнення таблиці
for _, row in df_sorted.iterrows():
    html_content += f"""
        <tr>
            <td>{row["Слово"]}</td>
            <td>{row["Частина мови"]}</td>
            <td>{row["Значення"]}</td>
            <td>{row["Приклад"]}</td>
            <td>{row["Сфера вживання"]}</td>
            <td>{row["Іншомовний відповідник"]}</td>
            <td>{row["Літературний відповідник"]}</td>
        </tr>
    """

# JavaScript фільтрація
html_content += """
        </tbody>
    </table>

<script>
function filterTable() {
    var input = document.getElementById("searchInput").value.toLowerCase();
    var domain = document.getElementById("domainSelect").value.toLowerCase();
    var pos = document.getElementById("posSelect").value.toLowerCase();
    var table = document.getElementById("dictionaryTable");
    var tr = table.getElementsByTagName("tr");
    var visibleCount = 0;

    for (var i = 1; i < tr.length; i++) {
        var tds = tr[i].getElementsByTagName("td");
        var word = tds[0].textContent.toLowerCase();
        var part = tds[1].textContent.toLowerCase();
        var meaning = tds[2].textContent.toLowerCase();
        var sphere = tds[4].textContent.toLowerCase();

        var wordMatch = word.includes(input) || meaning.includes(input);
        var domainMatch = (domain === "" || sphere === domain);
        var posMatch = (pos === "" || part === pos);

        if (wordMatch && domainMatch && posMatch) {
            tr[i].style.display = "";
            visibleCount++;
        } else {
            tr[i].style.display = "none";
        }
    }

    document.getElementById("noResults").style.display = visibleCount === 0 ? "block" : "none";
    document.getElementById("resultCount").innerText = "Знайдено результатів: " + visibleCount;
}

function clearFilters() {
    document.getElementById("searchInput").value = "";
    document.getElementById("domainSelect").value = "";
    document.getElementById("posSelect").value = "";
    filterTable();
}

window.onload = filterTable;
</script>

</body>
</html>
"""

# Збереження HTML
with open(r"C:\Users\Olga\PycharmProjects\dictionary\index.html", "w", encoding="utf-8") as f:
    f.write(html_content)
