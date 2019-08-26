from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def convert(bibtex):
    bibitem = ''
    r = bibtex.split('\n')
    i = 0
    while i < len(r):
        line = r[i].strip()
        if not line: i += 1
        if '@' == line[0]:
            code = line.split('{')[-1][:-1]
            title = venue = volume = number = pages = year = publisher = authors = None
            output_authors = []
            i += 1
            while i < len(r) and '@' not in r[i]:
                line = r[i].strip()
                # print(line)
                if line.startswith("title"):
                    title = line.split('{')[-1][:-2]
                elif line.startswith("journal"):
                    venue = line.split('{')[-1][:-2]
                elif line.startswith("volume"):
                    volume = line.split('{')[-1][:-2]
                elif line.startswith("number"):
                    number = line.split('{')[-1][:-2]
                elif line.startswith("pages"):
                    pages = line.split('{')[-1][:-2]
                elif line.startswith("year"):
                    year = line.split('{')[-1][:-2]
                elif line.startswith("publisher"):
                    publisher = line.split('{')[-1][:-2]
                elif line.startswith("author"):
                    authors = line[line.find("{") + 1:line.rfind("}")]
                    for LastFirst in authors.split('and'):
                        lf = LastFirst.replace(' ', '').split(',')
                        if len(lf) != 2: continue
                        last, first = lf[0], lf[1]
                        output_authors.append("{}, {}.".format(last.capitalize(), first.capitalize()[0]))
                i += 1

            bibitem += "\\bibitem{%s}" % code
            if len(output_authors) == 1:
                bibitem += str(output_authors[0] + " {}. ".format(title))
            else:
                bibitem += ", ".join(_ for _ in output_authors[:-1]) + " & " + output_authors[-1] + " {}. ".format(title)
            if venue:
                bibitem +="{{\\em {}}}.".format(" ".join([_.capitalize() for _ in venue.split(' ')]))
                if volume:
                    bibitem += " \\textbf{{{}}}".format(volume)
                if pages:
                    bibitem += ", {}".format(pages) if number else " pp. {}".format(pages)
                if year:
                    bibitem += " ({})".format(year)
            if publisher and not venue:
                bibitem += "({},{})".format(publisher, year)
    return bibitem

@app.route('/')
@app.route('/index')
def hello_world():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    bibitem = convert(request.form['text'])
    # redirect(url_for('index'))
    return '{}'.format(bibitem)

if __name__ == '__main__':
    app.run()