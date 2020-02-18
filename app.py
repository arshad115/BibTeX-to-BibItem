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
            title = venue = volume = number = pages = year = publisher = howpublished = note = authors = None
            output_authors = []
            i += 1
            while i < len(r) and '@' not in r[i]:
                line = r[i].strip()
                # print(line)
                if line.startswith("title"):
                    title = line[line.find("{") + 1:line.rfind("}")]
                elif line.startswith("journal"):
                    venue = line[line.find("{") + 1:line.rfind("}")]
                elif line.startswith("volume"):
                    volume = line[line.find("{") + 1:line.rfind("}")]
                elif line.startswith("number"):
                    number = line[line.find("{") + 1:line.rfind("}")]
                elif line.startswith("pages"):
                    pages = line[line.find("{") + 1:line.rfind("}")]
                elif line.startswith("year"):
                    year = line[line.find("{") + 1:line.rfind("}")]
                elif line.startswith("publisher"):
                    publisher = line[line.find("{") + 1:line.rfind("}")]
                elif line.startswith("howpublished"):
                    howpublished = line[line.find("{") + 1:line.rfind("}")]
                elif line.startswith("note"):
                    note = line[line.find("{") + 1:line.rfind("}")]
                elif line.startswith("author"):
                    authors = line[line.find("{") + 1:line.rfind("}")]
                    for LastFirst in authors.split('and'):
                        lf = LastFirst.replace(' ', '').split(',')
                        if len(lf) != 2:
                            output_authors.append("{}.".format(authors.capitalize()))
                        else:
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
            if not venue and not publisher and year:
                bibitem += " ({})".format(year)
            if howpublished:
                bibitem += ", {}".format(howpublished)
            if note:
                bibitem += ", {}".format(note)
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