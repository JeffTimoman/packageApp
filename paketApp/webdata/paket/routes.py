from flask import bluprint, render_template, request, redirect, url_for

paket = bluprint('paket', __name__)

@paket.route('/paket')
def paket():
    return "MOSHI MOSH"