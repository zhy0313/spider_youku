function Ea(b) {
    if (!b) return "";
    var b = b.toString(),
        e,
        c,
        g,
        d,
        f,
        h = [ - 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 62, -1, -1, -1, 63, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, -1, -1, -1, -1, -1, -1, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, -1, -1, -1, -1, -1, -1, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, -1, -1, -1, -1, -1];
    d = b.length;

    g = 0;
    for (f = ""; g < d;) {
        do {
            e = h[b.charCodeAt(g++) & 255];
            console.log(e)
        }
        while (g < d && -1 == e);

        if ( - 1 == e) break;

        do c = h[b.charCodeAt(g++) & 255];
        while (g < d && -1 == c);

        if ( - 1 == c) break;

        f += String.fromCharCode(e << 2 | (c & 48) >> 4);
        console.log([e << 2 | (c & 48) >> 4])
        console.log(f)
        do {
            e = b.charCodeAt(g++) & 255;
            if (61 == e) return f;
            e = h[e]
        } while ( g < d && - 1 == e );

        if ( - 1 == e) break;

        f += String.fromCharCode((c & 15) << 4 | (e & 60) >> 2);
        do {
            c = b.charCodeAt(g++) & 255;
            if (61 == c) return f;
            c = h[c]
        } while ( g < d && - 1 == c );

        if ( - 1 == c) break;

        f += String.fromCharCode((e & 3) << 6 | c)

    }
    return f
}

console.log(Ea('MwXXTQ4fLr3d0PbI9eJxU9b86BQ51w/KWBs='))
console.log(Ea('abcOK'))

a = 0

console.log(a++)
console.log(a++)
a = [19, 1, 4, 7, 30, 14, 28, 8, 24, 17, 6, 35, 34, 16, 9, 10, 13, 22, 32, 29, 31, 21, 18, 3, 2, 23, 25, 27, 11, 20, 5, 15, 12, 0, 33, 26]

console.log(a)



function O(b, e) {
    for (var c = [], g = 0; g < b.length; g++) {
        for (var d = 0,
                 d = "a" <= b[g] && "z" >= b[g] ? b[g].charCodeAt(0) - 97 : b[g] - 0 + 26, f = 0; 36 > f; f++) if (e[f] == d) {
            d = f;
            break
        }
        c[g] = 25 < d ? d - 26 : String.fromCharCode(d + 97)
    }
    return c.join("")
}

function N(b, e) {
    for (var c = [], g = 0, d, f = "", h = 0; 256 > h; h++) c[h] = h;
    for (h = 0; 256 > h; h++) g = (g + c[h] + b.charCodeAt(h % b.length)) % 256,
        d = c[h],
        c[h] = c[g],
        c[g] = d;
    for (var j = g = h = 0; j < e.length; j++) h = (h + 1) % 256,
        g = (g + c[h]) % 256,
        d = c[h],
        c[h] = c[g],
        c[g] = d,
        f += String.fromCharCode(e.charCodeAt(j) ^ c[(c[h] + c[g]) % 256]);
    return f
}

L = function (b) {
    if (!b) return "";
    var b = b.toString(),
        e,
        c,
        d,
        q,
        f,
        h;
    d = b.length;
    c = 0;
    for (e = ""; c < d;) {
        q = b.charCodeAt(c++) & 255;
        if (c == d) {
            e += "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".charAt(q >> 2);
            e += "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".charAt((q & 3) << 4);
            e += "==";
            break
        }
        f = b.charCodeAt(c++);
        if (c == d) {
            e += "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".charAt(q >> 2);
            e += "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".charAt((q & 3) << 4 | (f & 240) >> 4);
            e += "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".charAt((f & 15) << 2);
            e += "=";
            break
        }
        h = b.charCodeAt(c++);
        e += "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".charAt(q >> 2);
        e += "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".charAt((q & 3) << 4 | (f & 240) >> 4);
        e += "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".charAt((f & 15) << 2 | (h & 192) >> 6);
        e += "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".charAt(h & 63)
    }
    return e
}

console.log(Ea('MwXXTQ4fLr3d0PbI9eJxU9b86BQ51w/KWBs='))
a3 = "b4et"
a1 ='4'
encrypt_string = "MwXXTQ4fLr3d0PbI9eJxU9b86BQ51w/KWBs="
g = N(O(a3 + "o0b" + a1, [19, 1, 4, 7, 30, 14, 28, 8, 24, 17, 6, 35, 34, 16, 9, 10, 13, 22, 32, 29, 31, 21, 18, 3, 2, 23, 25, 27, 11, 20, 5, 15, 12, 0, 33, 26]).toString(), Ea(encrypt_string));

sid = g.split("_")[0];
token = g.split("_")[1];


b = 'XMTcwODg2OTQyMA=='

ep = encodeURIComponent(L(N(O("boa4" + "poz" + '1', [19, 1, 4, 7, 30, 14, 28, 8, 24, 17, 6, 35, 34, 16, 9, 10, 13, 22, 32, 29, 31, 21, 18, 3, 2, 23, 25, 27, 11, 20, 5, 15, 12, 0, 33, 26]).toString(), sid + "_" + b + "_" + token)));

console.log(ep)
console.log(sid)
console.log(token)

function newfile(ep,sid,token){
    var fso, f1, ts, s;
    var ForReading=1;
    fso=new ActiveXObject("Scripting.FileSystemObject");
    f1=fso.CreateTextFile("/Users/holysor/Desktop/youku_python/js/result.txt",true);
    f1.WriteLine("Hello World!");
    f1.WriteBlankLines(1);
    f1.Close();
}


var ep = encodeURIComponent(L(N(O("boa4" + "poz" + '1', [19, 1, 4, 7, 30, 14, 28, 8, 24, 17, 6, 35, 34, 16, 9, 10, 13, 22, 32, 29, 31, 21, 18, 3, 2, 23, 25, 27, 11, 20, 5, 15, 12, 0, 33, 26]).toString(), sid + "_" + b + "_" + token)));



