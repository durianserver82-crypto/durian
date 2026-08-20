import telebot
import requests
import json
import time
import threading
import re
from telebot import types
from datetime import datetime
import os

print("🚀 বট লোড হচ্ছে...")

# ============= আপনার ডেটা =============
BOT_TOKEN = os.environ.get('BOT_TOKEN', "8727135279:AAHlZ9uj5aRCLca1J8HrKyPmVtwXX-eooxI")
USERNAME = os.environ.get('USERNAME', "noobxvau")
API_KEY = os.environ.get('API_KEY', "WHUwNkg1WnVOM1pBc0lKN0ZBeENWQT09")
API_BASE_URL = "https://api.durianrcs.com/out/ext_api"

# ============= প্রোজেক্ট সেটিংস =============
DEFAULT_PID = "0257"
DEFAULT_SERIAL = "2"  # ডিফল্ট সিরিয়াল (সব)
MAX_RETRIES = 30
RETRY_DELAY = 2
OTP_CHECK_INTERVAL = 5
OTP_TIMEOUT = 300

# ============= গ্রুপ ও ইউজার সেটিংস =============
GROUP_ID = -1003960397555  # OTP গ্রুপ আইডি

# অনুমোদিত ইউজারদের চ্যাট আইডি
ALLOWED_USERS = [
    8000000507,
    # এখানে আপনার চ্যাট আইডি দিন
    # 123456789,
]

print("✅ কনফিগারেশন লোড হয়েছে")

# ============= সাপোর্টেড কান্ট্রি লিস্ট =============
COUNTRIES = [
    {"serial": "1", "name": "Argentina", "cuy": "ar", "short": ["arg", "argentina"]},
    {"serial": "2", "name": "Australia", "cuy": "au", "short": ["aus", "australia"]},
    {"serial": "3", "name": "Austria", "cuy": "at", "short": ["aut", "austria"]},
    {"serial": "4", "name": "Bahrain", "cuy": "bh", "short": ["bhr", "bahrain"]},
    {"serial": "5", "name": "Brazil", "cuy": "br", "short": ["bra", "brazil"]},
    {"serial": "6", "name": "Chile", "cuy": "cl", "short": ["chl", "chile"]},
    {"serial": "7", "name": "Colombia", "cuy": "co", "short": ["col", "colombia"]},
    {"serial": "8", "name": "Czech Republic", "cuy": "cz", "short": ["cze", "czech"]},
    {"serial": "9", "name": "Ecuador", "cuy": "ec", "short": ["ecu", "ecuador"]},
    {"serial": "10", "name": "Finland", "cuy": "fi", "short": ["fin", "finland"]},
    {"serial": "11", "name": "France", "cuy": "fr", "short": ["fra", "france"]},
    {"serial": "12", "name": "Germany", "cuy": "de", "short": ["deu", "germany"]},
    {"serial": "13", "name": "Ghana", "cuy": "gh", "short": ["gha", "ghana"]},
    {"serial": "14", "name": "Hungary", "cuy": "hu", "short": ["hun", "hungary"]},
    {"serial": "15", "name": "India", "cuy": "in", "short": ["ind", "india"]},
    {"serial": "16", "name": "Indonesia", "cuy": "id", "short": ["idn", "indonesia"]},
    {"serial": "17", "name": "Ireland", "cuy": "ie", "short": ["irl", "ireland"]},
    {"serial": "18", "name": "Japan", "cuy": "jp", "short": ["jpn", "japan"]},
    {"serial": "19", "name": "Jordan", "cuy": "jo", "short": ["jor", "jordan"]},
    {"serial": "20", "name": "Kenya", "cuy": "ke", "short": ["ken", "kenya"]},
    {"serial": "21", "name": "Luxembourg", "cuy": "lu", "short": ["lux", "luxembourg"]},
    {"serial": "22", "name": "Malaysia", "cuy": "my", "short": ["mys", "malaysia"]},
    {"serial": "23", "name": "Mexico", "cuy": "mx", "short": ["mex", "mexico"]},
    {"serial": "24", "name": "Netherlands", "cuy": "nl", "short": ["nld", "netherlands"]},
    {"serial": "25", "name": "Nigeria", "cuy": "ng", "short": ["nga", "nigeria"]},
    {"serial": "26", "name": "Norway", "cuy": "no", "short": ["nor", "norway"]},
    {"serial": "27", "name": "Panama", "cuy": "pa", "short": ["pan", "panama"]},
    {"serial": "28", "name": "Philippines", "cuy": "ph", "short": ["phl", "philippines"]},
    {"serial": "29", "name": "Poland", "cuy": "pl", "short": ["pol", "poland"]},
    {"serial": "30", "name": "Portugal", "cuy": "pt", "short": ["prt", "portugal"]},
    {"serial": "31", "name": "Romania", "cuy": "ro", "short": ["rou", "romania"]},
    {"serial": "32", "name": "Saudi Arabia", "cuy": "sa", "short": ["sau", "saudi"]},
    {"serial": "33", "name": "Singapore", "cuy": "sg", "short": ["sgp", "singapore"]},
    {"serial": "34", "name": "Vietnam", "cuy": "vn", "short": ["vnm", "vietnam"]},
    {"serial": "35", "name": "Slovenia", "cuy": "si", "short": ["svn", "slovenia"]},
    {"serial": "36", "name": "South Africa", "cuy": "za", "short": ["zaf", "southafrica"]},
    {"serial": "37", "name": "Spain", "cuy": "es", "short": ["esp", "spain"]},
    {"serial": "38", "name": "Switzerland", "cuy": "ch", "short": ["che", "switzerland"]},
    {"serial": "39", "name": "Thailand", "cuy": "th", "short": ["tha", "thailand"]},
    {"serial": "40", "name": "United Arab Emirates", "cuy": "ae", "short": ["are", "uae"]},
    {"serial": "41", "name": "Macedonia", "cuy": "mk", "short": ["mkd", "macedonia"]},
    {"serial": "42", "name": "Egypt", "cuy": "eg", "short": ["egy", "egypt"]},
    {"serial": "43", "name": "United States", "cuy": "us", "short": ["usa", "us", "america"]},
    {"serial": "44", "name": "Andorra", "cuy": "ad", "short": ["and", "andorra"]},
    {"serial": "45", "name": "Afghanistan", "cuy": "af", "short": ["afg", "afghanistan"]},
    {"serial": "46", "name": "Antigua and Barbuda", "cuy": "ag", "short": ["atg", "antigua"]},
    {"serial": "47", "name": "Anguilla", "cuy": "ai", "short": ["aia", "anguilla"]},
    {"serial": "48", "name": "Albania", "cuy": "al", "short": ["alb", "albania"]},
    {"serial": "49", "name": "Armenia", "cuy": "am", "short": ["arm", "armenia"]},
    {"serial": "50", "name": "Angola", "cuy": "ao", "short": ["ago", "angola"]},
    {"serial": "51", "name": "American Samoa", "cuy": "as", "short": ["asm", "americansamoa"]},
    {"serial": "52", "name": "Aruba", "cuy": "aw", "short": ["abw", "aruba"]},
    {"serial": "53", "name": "Azerbaijan", "cuy": "az", "short": ["aze", "azerbaijan"]},
    {"serial": "54", "name": "Bosnia and Herzegovina", "cuy": "ba", "short": ["bih", "bosnia"]},
    {"serial": "55", "name": "Barbados", "cuy": "bb", "short": ["brb", "barbados"]},
    {"serial": "56", "name": "Bangladesh", "cuy": "bd", "short": ["bgd", "bangladesh"]},
    {"serial": "57", "name": "Belgium", "cuy": "be", "short": ["bel", "belgium"]},
    {"serial": "58", "name": "Burkina Faso", "cuy": "bf", "short": ["bfa", "burkina"]},
    {"serial": "59", "name": "Bulgaria", "cuy": "bg", "short": ["bgr", "bulgaria"]},
    {"serial": "60", "name": "Burundi", "cuy": "bi", "short": ["bdi", "burundi"]},
    {"serial": "61", "name": "Benin", "cuy": "bj", "short": ["ben", "benin"]},
    {"serial": "62", "name": "Bermuda", "cuy": "bm", "short": ["bmu", "bermuda"]},
    {"serial": "63", "name": "Brunei", "cuy": "bn", "short": ["brn", "brunei"]},
    {"serial": "64", "name": "Bolivia", "cuy": "bo", "short": ["bol", "bolivia"]},
    {"serial": "65", "name": "Bahamas", "cuy": "bs", "short": ["bhs", "bahamas"]},
    {"serial": "66", "name": "Bhutan", "cuy": "bt", "short": ["btn", "bhutan"]},
    {"serial": "67", "name": "Botswana", "cuy": "bw", "short": ["bwa", "botswana"]},
    {"serial": "68", "name": "Belarus", "cuy": "by", "short": ["blr", "belarus"]},
    {"serial": "69", "name": "Belize", "cuy": "bz", "short": ["blz", "belize"]},
    {"serial": "70", "name": "Canada", "cuy": "ca", "short": ["can", "canada"]},
    {"serial": "71", "name": "Congo DR", "cuy": "cd", "short": ["cod", "congodr"]},
    {"serial": "72", "name": "Central African Republic", "cuy": "cf", "short": ["caf", "centralafrican"]},
    {"serial": "73", "name": "Congo", "cuy": "cg", "short": ["cog", "congo"]},
    {"serial": "74", "name": "Cote d'Ivoire", "cuy": "ci", "short": ["civ", "ivorycoast"]},
    {"serial": "75", "name": "Cook Islands", "cuy": "ck", "short": ["cok", "cookislands"]},
    {"serial": "76", "name": "Cameroon", "cuy": "cm", "short": ["cmr", "cameroon"]},
    {"serial": "77", "name": "Costa Rica", "cuy": "cr", "short": ["cri", "costarica"]},
    {"serial": "78", "name": "Cuba", "cuy": "cu", "short": ["cub", "cuba"]},
    {"serial": "79", "name": "Cape Verde", "cuy": "cv", "short": ["cpv", "capeverde"]},
    {"serial": "80", "name": "Curacao", "cuy": "cw", "short": ["cuw", "curacao"]},
    {"serial": "81", "name": "Cyprus", "cuy": "cy", "short": ["cyp", "cyprus"]},
    {"serial": "82", "name": "Djibouti", "cuy": "dj", "short": ["dji", "djibouti"]},
    {"serial": "83", "name": "Denmark", "cuy": "dk", "short": ["dnk", "denmark"]},
    {"serial": "84", "name": "Dominica", "cuy": "dm", "short": ["dma", "dominica"]},
    {"serial": "85", "name": "Dominican Republic", "cuy": "do", "short": ["dom", "dominican"]},
    {"serial": "86", "name": "Algeria", "cuy": "dz", "short": ["dza", "algeria"]},
    {"serial": "87", "name": "Estonia", "cuy": "ee", "short": ["est", "estonia"]},
    {"serial": "88", "name": "Eritrea", "cuy": "er", "short": ["eri", "eritrea"]},
    {"serial": "89", "name": "Ethiopia", "cuy": "et", "short": ["eth", "ethiopia"]},
    {"serial": "90", "name": "Fiji", "cuy": "fj", "short": ["fji", "fiji"]},
    {"serial": "91", "name": "Falkland Islands", "cuy": "fk", "short": ["flk", "falkland"]},
    {"serial": "92", "name": "Micronesia", "cuy": "fm", "short": ["fsm", "micronesia"]},
    {"serial": "93", "name": "Faroe Islands", "cuy": "fo", "short": ["fro", "faroe"]},
    {"serial": "94", "name": "Gabon", "cuy": "ga", "short": ["gab", "gabon"]},
    {"serial": "95", "name": "United Kingdom", "cuy": "gb", "short": ["gbr", "uk", "britain"]},
    {"serial": "96", "name": "Grenada", "cuy": "gd", "short": ["grd", "grenada"]},
    {"serial": "97", "name": "Georgia", "cuy": "ge", "short": ["geo", "georgia"]},
    {"serial": "98", "name": "French Guiana", "cuy": "gf", "short": ["guf", "frenchguiana"]},
    {"serial": "99", "name": "Gibraltar", "cuy": "gi", "short": ["gib", "gibraltar"]},
    {"serial": "100", "name": "Greenland", "cuy": "gl", "short": ["grl", "greenland"]},
    {"serial": "101", "name": "Gambia", "cuy": "gm", "short": ["gmb", "gambia"]},
    {"serial": "102", "name": "Guinea", "cuy": "gn", "short": ["gin", "guinea"]},
    {"serial": "103", "name": "Equatorial Guinea", "cuy": "gq", "short": ["gnq", "equatorialguinea"]},
    {"serial": "104", "name": "Greece", "cuy": "gr", "short": ["grc", "greece"]},
    {"serial": "105", "name": "Guatemala", "cuy": "gt", "short": ["gtm", "guatemala"]},
    {"serial": "106", "name": "Guam", "cuy": "gu", "short": ["gum", "guam"]},
    {"serial": "107", "name": "Guinea-Bissau", "cuy": "gw", "short": ["gnb", "guineabissau"]},
    {"serial": "108", "name": "Guyana", "cuy": "gy", "short": ["guy", "guyana"]},
    {"serial": "109", "name": "Honduras", "cuy": "hn", "short": ["hnd", "honduras"]},
    {"serial": "110", "name": "Croatia", "cuy": "hr", "short": ["hrv", "croatia"]},
    {"serial": "111", "name": "Haiti", "cuy": "ht", "short": ["hti", "haiti"]},
    {"serial": "112", "name": "Israel", "cuy": "il", "short": ["isr", "israel"]},
    {"serial": "113", "name": "Iraq", "cuy": "iq", "short": ["irq", "iraq"]},
    {"serial": "114", "name": "Iran", "cuy": "ir", "short": ["irn", "iran"]},
    {"serial": "115", "name": "Iceland", "cuy": "is", "short": ["isl", "iceland"]},
    {"serial": "116", "name": "Italy", "cuy": "it", "short": ["ita", "italy"]},
    {"serial": "117", "name": "Jamaica", "cuy": "jm", "short": ["jam", "jamaica"]},
    {"serial": "118", "name": "Kyrgyzstan", "cuy": "kg", "short": ["kgz", "kyrgyzstan"]},
    {"serial": "119", "name": "Cambodia", "cuy": "kh", "short": ["khm", "cambodia"]},
    {"serial": "120", "name": "Kiribati", "cuy": "ki", "short": ["kir", "kiribati"]},
    {"serial": "121", "name": "Comoros", "cuy": "km", "short": ["com", "comoros"]},
    {"serial": "122", "name": "Saint Kitts and Nevis", "cuy": "kn", "short": ["kna", "saintkitts"]},
    {"serial": "123", "name": "North Korea", "cuy": "kp", "short": ["prk", "northkorea"]},
    {"serial": "124", "name": "South Korea", "cuy": "kr", "short": ["kor", "southkorea"]},
    {"serial": "125", "name": "Kuwait", "cuy": "kw", "short": ["kwt", "kuwait"]},
    {"serial": "126", "name": "Cayman Islands", "cuy": "ky", "short": ["cym", "cayman"]},
    {"serial": "127", "name": "Kazakhstan", "cuy": "kz", "short": ["kaz", "kazakhstan"]},
    {"serial": "128", "name": "Laos", "cuy": "la", "short": ["lao", "laos"]},
    {"serial": "129", "name": "Lebanon", "cuy": "lb", "short": ["lbn", "lebanon"]},
    {"serial": "130", "name": "Saint Lucia", "cuy": "lc", "short": ["lca", "saintlucia"]},
    {"serial": "131", "name": "Liechtenstein", "cuy": "li", "short": ["lie", "liechtenstein"]},
    {"serial": "132", "name": "Sri Lanka", "cuy": "lk", "short": ["lka", "srilanka"]},
    {"serial": "133", "name": "Liberia", "cuy": "lr", "short": ["lbr", "liberia"]},
    {"serial": "134", "name": "Lesotho", "cuy": "ls", "short": ["lso", "lesotho"]},
    {"serial": "135", "name": "Lithuania", "cuy": "lt", "short": ["ltu", "lithuania"]},
    {"serial": "136", "name": "Latvia", "cuy": "lv", "short": ["lva", "latvia"]},
    {"serial": "137", "name": "Libya", "cuy": "ly", "short": ["lby", "libya"]},
    {"serial": "138", "name": "Morocco", "cuy": "ma", "short": ["mar", "morocco"]},
    {"serial": "139", "name": "Monaco", "cuy": "mc", "short": ["mco", "monaco"]},
    {"serial": "140", "name": "Moldova", "cuy": "md", "short": ["mda", "moldova"]},
    {"serial": "141", "name": "Montenegro", "cuy": "me", "short": ["mne", "montenegro"]},
    {"serial": "142", "name": "Madagascar", "cuy": "mg", "short": ["mdg", "madagascar"]},
    {"serial": "143", "name": "Marshall Islands", "cuy": "mh", "short": ["mhl", "marshall"]},
    {"serial": "144", "name": "Mali", "cuy": "ml", "short": ["mli", "mali"]},
    {"serial": "145", "name": "Myanmar", "cuy": "mm", "short": ["mmr", "myanmar"]},
    {"serial": "146", "name": "Mongolia", "cuy": "mn", "short": ["mng", "mongolia"]},
    {"serial": "147", "name": "Macao", "cuy": "mo", "short": ["mac", "macao"]},
    {"serial": "148", "name": "Northern Mariana Islands", "cuy": "mp", "short": ["mnp", "northernmariana"]},
    {"serial": "149", "name": "Martinique", "cuy": "mq", "short": ["mtq", "martinique"]},
    {"serial": "150", "name": "Mauritania", "cuy": "mr", "short": ["mrt", "mauritania"]},
    {"serial": "151", "name": "Montserrat", "cuy": "ms", "short": ["msr", "montserrat"]},
    {"serial": "152", "name": "Malta", "cuy": "mt", "short": ["mlt", "malta"]},
    {"serial": "153", "name": "Mauritius", "cuy": "mu", "short": ["mus", "mauritius"]},
    {"serial": "154", "name": "Maldives", "cuy": "mv", "short": ["mdv", "maldives"]},
    {"serial": "155", "name": "Malawi", "cuy": "mw", "short": ["mwi", "malawi"]},
    {"serial": "156", "name": "Mozambique", "cuy": "mz", "short": ["moz", "mozambique"]},
    {"serial": "157", "name": "Namibia", "cuy": "na", "short": ["nam", "namibia"]},
    {"serial": "158", "name": "New Caledonia", "cuy": "nc", "short": ["ncl", "newcaledonia"]},
    {"serial": "159", "name": "Niger", "cuy": "ne", "short": ["ner", "niger"]},
    {"serial": "160", "name": "Nicaragua", "cuy": "ni", "short": ["nic", "nicaragua"]},
    {"serial": "161", "name": "Nepal", "cuy": "np", "short": ["npl", "nepal"]},
    {"serial": "162", "name": "Nauru", "cuy": "nr", "short": ["nru", "nauru"]},
    {"serial": "163", "name": "Niue", "cuy": "nu", "short": ["niu", "niue"]},
    {"serial": "164", "name": "New Zealand", "cuy": "nz", "short": ["nzl", "newzealand"]},
    {"serial": "165", "name": "Oman", "cuy": "om", "short": ["omn", "oman"]},
    {"serial": "166", "name": "Peru", "cuy": "pe", "short": ["per", "peru"]},
    {"serial": "167", "name": "French Polynesia", "cuy": "pf", "short": ["pyf", "frenchpolynesia"]},
    {"serial": "168", "name": "Papua New Guinea", "cuy": "pg", "short": ["png", "papuanewguinea"]},
    {"serial": "169", "name": "Pakistan", "cuy": "pk", "short": ["pak", "pakistan"]},
    {"serial": "170", "name": "Saint Pierre and Miquelon", "cuy": "pm", "short": ["spm", "saintpierre"]},
    {"serial": "171", "name": "Puerto Rico", "cuy": "pr", "short": ["pri", "puertorico"]},
    {"serial": "172", "name": "Palestine", "cuy": "ps", "short": ["pse", "palestine"]},
    {"serial": "173", "name": "Palau", "cuy": "pw", "short": ["plw", "palau"]},
    {"serial": "174", "name": "Paraguay", "cuy": "py", "short": ["pry", "paraguay"]},
    {"serial": "175", "name": "Qatar", "cuy": "qa", "short": ["qat", "qatar"]},
    {"serial": "176", "name": "Reunion", "cuy": "re", "short": ["reu", "reunion"]},
    {"serial": "177", "name": "Serbia", "cuy": "rs", "short": ["srb", "serbia"]},
    {"serial": "178", "name": "Russia", "cuy": "ru", "short": ["rus", "russia"]},
    {"serial": "179", "name": "Rwanda", "cuy": "rw", "short": ["rwa", "rwanda"]},
    {"serial": "180", "name": "Solomon Islands", "cuy": "sb", "short": ["slb", "solomon"]},
    {"serial": "181", "name": "Seychelles", "cuy": "sc", "short": ["syc", "seychelles"]},
    {"serial": "182", "name": "Sudan", "cuy": "sd", "short": ["sdn", "sudan"]},
    {"serial": "183", "name": "Sweden", "cuy": "se", "short": ["swe", "sweden"]},
    {"serial": "184", "name": "Slovakia", "cuy": "sk", "short": ["svk", "slovakia"]},
    {"serial": "185", "name": "Sierra Leone", "cuy": "sl", "short": ["sle", "sierraleone"]},
    {"serial": "186", "name": "San Marino", "cuy": "sm", "short": ["smr", "sanmarino"]},
    {"serial": "187", "name": "Senegal", "cuy": "sn", "short": ["sen", "senegal"]},
    {"serial": "188", "name": "Somalia", "cuy": "so", "short": ["som", "somalia"]},
    {"serial": "189", "name": "Suriname", "cuy": "sr", "short": ["sur", "suriname"]},
    {"serial": "190", "name": "South Sudan", "cuy": "ss", "short": ["ssd", "southsudan"]},
    {"serial": "191", "name": "Sao Tome and Principe", "cuy": "st", "short": ["stp", "saotome"]},
    {"serial": "192", "name": "El Salvador", "cuy": "sv", "short": ["slv", "elsalvador"]},
    {"serial": "193", "name": "Syria", "cuy": "sy", "short": ["syr", "syria"]},
    {"serial": "194", "name": "Swaziland", "cuy": "sz", "short": ["swz", "swaziland"]},
    {"serial": "195", "name": "Turks and Caicos", "cuy": "tc", "short": ["tca", "turksandcaicos"]},
    {"serial": "196", "name": "Chad", "cuy": "td", "short": ["tcd", "chad"]},
    {"serial": "197", "name": "Togo", "cuy": "tg", "short": ["tgo", "togo"]},
    {"serial": "198", "name": "Tajikistan", "cuy": "tj", "short": ["tjk", "tajikistan"]},
    {"serial": "199", "name": "Timor-Leste", "cuy": "tl", "short": ["tls", "timor"]},
    {"serial": "200", "name": "Turkmenistan", "cuy": "tm", "short": ["tkm", "turkmenistan"]},
    {"serial": "201", "name": "Tunisia", "cuy": "tn", "short": ["tun", "tunisia"]},
    {"serial": "202", "name": "Tonga", "cuy": "to", "short": ["ton", "tonga"]},
    {"serial": "203", "name": "Turkey", "cuy": "tr", "short": ["tur", "turkey"]},
    {"serial": "204", "name": "Trinidad and Tobago", "cuy": "tt", "short": ["tto", "trinidad"]},
    {"serial": "205", "name": "Tanzania", "cuy": "tz", "short": ["tza", "tanzania"]},
    {"serial": "206", "name": "Ukraine", "cuy": "ua", "short": ["ukr", "ukraine"]},
    {"serial": "207", "name": "Uganda", "cuy": "ug", "short": ["uga", "uganda"]},
    {"serial": "208", "name": "Uruguay", "cuy": "uy", "short": ["ury", "uruguay"]},
    {"serial": "209", "name": "Uzbekistan", "cuy": "uz", "short": ["uzb", "uzbekistan"]},
    {"serial": "210", "name": "Vatican City", "cuy": "va", "short": ["vat", "vatican"]},
    {"serial": "211", "name": "Saint Vincent", "cuy": "vc", "short": ["vct", "saintvincent"]},
    {"serial": "212", "name": "Venezuela", "cuy": "ve", "short": ["ven", "venezuela"]},
    {"serial": "213", "name": "British Virgin Islands", "cuy": "vg", "short": ["vgb", "britishvirgin"]},
    {"serial": "214", "name": "US Virgin Islands", "cuy": "vi", "short": ["vir", "usvirgin"]},
    {"serial": "215", "name": "Vanuatu", "cuy": "vu", "short": ["vut", "vanuatu"]},
    {"serial": "216", "name": "Wallis and Futuna", "cuy": "wf", "short": ["wlf", "wallis"]},
    {"serial": "217", "name": "Samoa", "cuy": "ws", "short": ["wsm", "samoa"]},
    {"serial": "218", "name": "Yemen", "cuy": "ye", "short": ["yem", "yemen"]},
    {"serial": "219", "name": "Zambia", "cuy": "zm", "short": ["zmb", "zambia"]},
    {"serial": "220", "name": "Zimbabwe", "cuy": "zw", "short": ["zwe", "zimbabwe"]},
    {"serial": "221", "name": "Kosovo", "cuy": "xk", "short": ["ksa", "kosovo"]},
    {"serial": "222", "name": "Netherlands Antilles", "cuy": "an", "short": ["ant", "netherlandsantilles"]},
    {"serial": "223", "name": "United Kingdom", "cuy": "uk", "short": ["gbr", "uk", "britain", "england"]},
]

print(f"✅ {len(COUNTRIES)}টি দেশ লোড হয়েছে")

# ============= বট =============
bot = telebot.TeleBot(BOT_TOKEN)
user_data = {}
monitoring_threads = {}
user_states = {}
user_country = {}
user_search = {}
running_threads = {}  # নাম্বার জেনারেশন থ্রেড ট্র্যাক করার জন্য
user_serials = {}  # প্রতিটি ইউজারের সিরিয়াল লিস্ট সংরক্ষণ

# ============= ইউজার চেক ফাংশন =============
def is_user_allowed(user_id):
    if not ALLOWED_USERS:
        return True
    return user_id in ALLOWED_USERS

def get_user_identifier(message):
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name    
    if username:
        return f"@{username} (ID: {user_id})"
    else:
        return f"{first_name} (ID: {user_id})"

# ============= সিরিয়াল ফাংশন =============
def get_user_serials(chat_id):
    """ইউজারের সেট করা সিরিয়াল লিস্ট রিটার্ন করে, না থাকলে ['2'] (সব)"""
    chat_id_str = str(chat_id)
    if chat_id_str in user_serials and user_serials[chat_id_str]:
        return user_serials[chat_id_str]
    return [DEFAULT_SERIAL]

def format_serials_display(serials):
    """সিরিয়াল লিস্টকে সুন্দরভাবে দেখানোর জন্য"""
    if not serials or serials == [DEFAULT_SERIAL]:
        return "সব সিরিয়াল (ডিফল্ট)"
    return ", ".join(serials)

# ============= কী-বোর্ড =============
def get_main_keyboard():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton('📱 Get Number')
    btn2 = types.KeyboardButton('💰 Balance')
    btn3 = types.KeyboardButton('📊 Status')
    btn4 = types.KeyboardButton('🗑️ Clear All')
    btn5 = types.KeyboardButton('ℹ️ Help')
    btn6 = types.KeyboardButton('🔍 Search Country')
    btn7 = types.KeyboardButton('📜 Active Numbers')
    btn8 = types.KeyboardButton('🛑 Stop & Show Numbers')
    btn9 = types.KeyboardButton('🔢 Set Serial')
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9)
    return markup

# ============= API কল =============
def call_api(endpoint, params=None):
    try:
        url = f"{API_BASE_URL}/{endpoint}"
        if params:
            filtered_params = {k: v for k, v in params.items() if v is not None and v != 'null'}
            url += "?" + "&".join([f"{k}={v}" for k, v in filtered_params.items()])
        print(f"📡 {url}")
        response = requests.get(url, timeout=15)
        return response.json()
    except Exception as e:
        print(f"❌ {e}")
        return {'code': 500, 'msg': str(e)}

# ============= কান্ট্রি সার্চ =============
def search_country(query):
    query = query.lower().strip()
    results = []
    
    for country in COUNTRIES:
        if query in country['name'].lower():
            results.append(country)
        elif any(query in short.lower() for short in country.get('short', [])):
            results.append(country)
        elif query == country['cuy'].lower():
            results.append(country)
        elif query == country['serial']:
            results.append(country)
    
    return results

@bot.message_handler(func=lambda message: message.text == '🔍 Search Country')
def search_country_prompt(message):
    chat_id = message.chat.id
    
    if not is_user_allowed(message.from_user.id):
        bot.send_message(chat_id, "⛔ আপনি এই বট ব্যবহার করার অনুমতি পাননি!")
        return
    
    user_search[str(chat_id)] = True
    bot.send_message(chat_id, 
        "🔍 *কান্ট্রি খুঁজুন:*\n\n"
        "কান্ট্রির নাম বা শর্টকাট লিখুন।\n"
        "যেমন: `bd`, `bangladesh`, `us`, `india`, `uk`\n\n"
        f"📌 *মোট {len(COUNTRIES)}টি দেশ উপলব্ধ*",
        parse_mode='Markdown'
    )

# ============= সিরিয়াল সেট করার হ্যান্ডলার =============
@bot.message_handler(func=lambda message: message.text == '🔢 Set Serial')
def set_serial_prompt(message):
    chat_id = message.chat.id
    
    if not is_user_allowed(message.from_user.id):
        bot.send_message(chat_id, "⛔ আপনি এই বট ব্যবহার করার অনুমতি পাননি!")
        return
    
    current_serials = get_user_serials(chat_id)
    country = user_country.get(str(chat_id), {'name': 'Bangladesh', 'cuy': 'bd'})
    
    markup = types.InlineKeyboardMarkup(row_width=3)
    markup.add(
        types.InlineKeyboardButton("➕ একাধিক সিরিয়াল", callback_data="add_serials"),
        types.InlineKeyboardButton("🔄 রিসেট (সব)", callback_data="reset_serials"),
        types.InlineKeyboardButton("📋 দেখুন", callback_data="view_serials")
    )
    
    bot.send_message(chat_id,
        f"🔢 *সিরিয়াল সেটিংস*\n\n"
        f"🌍 বর্তমান দেশ: {country['name']}\n"
        f"📌 বর্তমান সিরিয়াল: {format_serials_display(current_serials)}\n\n"
        f"*নিয়ম:*\n"
        f"• সিরিয়াল কমা দিয়ে আলাদা করুন\n"
        f"• যেমন: `93,91,96`\n"
        f"• ডিফল্ট (সব): `2`\n\n"
        f"📝 *সিরিয়াল সেট করতে টাইপ করুন:*\n"
        f"`/setserial 93,91,96`\n"
        f"অথবা নিচের বাটন ব্যবহার করুন",
        parse_mode='Markdown',
        reply_markup=markup
    )
    
    user_states[str(chat_id)] = 'waiting_serial'

@bot.message_handler(commands=['setserial'])
def set_serial_command(message):
    chat_id = message.chat.id
    
    if not is_user_allowed(message.from_user.id):
        bot.send_message(chat_id, "⛔ আপনি এই বট ব্যবহার করার অনুমতি পাননি!")
        return
    
    try:
        # কমান্ড থেকে আর্গুমেন্ট নেওয়া
        args = message.text.split(' ', 1)
        if len(args) < 2:
            bot.send_message(chat_id, 
                "❌ *সঠিক ফরম্যাট:* `/setserial 93,91,96`\n\n"
                "📌 একাধিক সিরিয়াল কমা দিয়ে আলাদা করুন\n"
                "যেমন: `/setserial 93,91,96`\n"
                "ডিফল্ট (সব): `/setserial 2`",
                parse_mode='Markdown'
            )
            return
        
        serials_text = args[1].strip()
        serials = [s.strip() for s in serials_text.split(',') if s.strip()]
        
        # সিরিয়াল ভ্যালিডেশন
        valid_serials = []
        for s in serials:
            if s.isdigit() and len(s) <= 3:
                valid_serials.append(s)
            else:
                bot.send_message(chat_id, f"❌ `{s}` সঠিক সিরিয়াল নয়! (শুধু সংখ্যা দিন)")
                return
        
        if not valid_serials:
            bot.send_message(chat_id, "❌ কোনো সঠিক সিরিয়াল পাওয়া যায়নি!")
            return
        
        # সিরিয়াল সেভ করা
        user_serials[str(chat_id)] = valid_serials
        bot.send_message(chat_id,
            f"✅ *সিরিয়াল সেট করা হয়েছে!*\n\n"
            f"📌 সিরিয়াল: {format_serials_display(valid_serials)}\n"
            f"🌍 দেশ: {user_country.get(str(chat_id), {}).get('name', 'N/A')}\n\n"
            f"📱 এখন 'Get Number' ক্লিক করলে এই সিরিয়ালের নাম্বার আসবে",
            parse_mode='Markdown'
        )
        
    except Exception as e:
        bot.send_message(chat_id, f"❌ {str(e)}")

@bot.message_handler(commands=['resetserial'])
def reset_serial_command(message):
    chat_id = message.chat.id
    
    if not is_user_allowed(message.from_user.id):
        bot.send_message(chat_id, "⛔ আপনি এই বট ব্যবহার করার অনুমতি পাননি!")
        return
    
    if str(chat_id) in user_serials:
        del user_serials[str(chat_id)]
    
    bot.send_message(chat_id,
        "🔄 *সিরিয়াল রিসেট করা হয়েছে!*\n\n"
        f"📌 এখন সব সিরিয়ালের নাম্বার আসবে (ডিফল্ট: {DEFAULT_SERIAL})",
        parse_mode='Markdown'
    )

@bot.message_handler(commands=['viewserial'])
def view_serial_command(message):
    chat_id = message.chat.id
    
    if not is_user_allowed(message.from_user.id):
        bot.send_message(chat_id, "⛔ আপনি এই বট ব্যবহার করার অনুমতি পাননি!")
        return
    
    serials = get_user_serials(chat_id)
    country = user_country.get(str(chat_id), {}).get('name', 'N/A')
    
    bot.send_message(chat_id,
        f"📋 *বর্তমান সিরিয়াল*\n\n"
        f"🌍 দেশ: {country}\n"
        f"📌 সিরিয়াল: {format_serials_display(serials)}\n\n"
        f"🔢 *সিরিয়াল পরিবর্তন করতে:* `/setserial 93,91`",
        parse_mode='Markdown'
    )

# ============= টেক্সট হ্যান্ডলার =============
@bot.message_handler(func=lambda message: True)
def handle_text_messages(message):
    chat_id = message.chat.id
    
    if not is_user_allowed(message.from_user.id):
        bot.send_message(chat_id, "⛔ আপনি এই বট ব্যবহার করার অনুমতি পাননি!")
        return
    
    text = message.text
    
    # সিরিয়াল ওয়েটিং স্টেট
    if user_states.get(str(chat_id)) == 'waiting_serial' and text != '🔢 Set Serial':
        if text.startswith('/'):
            return
        # টেক্সট থেকে সিরিয়াল পার্স করা
        serials = [s.strip() for s in text.split(',') if s.strip()]
        valid_serials = []
        for s in serials:
            if s.isdigit() and len(s) <= 3:
                valid_serials.append(s)
        
        if valid_serials:
            user_serials[str(chat_id)] = valid_serials
            user_states[str(chat_id)] = None
            bot.send_message(chat_id,
                f"✅ *সিরিয়াল সেট করা হয়েছে!*\n\n"
                f"📌 সিরিয়াল: {format_serials_display(valid_serials)}",
                parse_mode='Markdown',
                reply_markup=get_main_keyboard()
            )
        else:
            bot.send_message(chat_id, "❌ সঠিক সিরিয়াল দিন! যেমন: `93,91,96`")
        return
    
    if str(chat_id) in user_search and user_search[str(chat_id)]:
        results = search_country(text)
        
        if results:
            markup = types.InlineKeyboardMarkup(row_width=2)
            for country in results[:20]:
                btn = types.InlineKeyboardButton(
                    f"🌍 {country['name']} ({country['cuy'].upper()})", 
                    callback_data=f"country_{country['serial']}_{country['cuy']}"
                )
                markup.add(btn)
            
            btn_cancel = types.InlineKeyboardButton("❌ বাতিল", callback_data="cancel")
            markup.add(btn_cancel)
            
            user_search[str(chat_id)] = False
            bot.send_message(chat_id, 
                f"🔍 *'{text}' এর জন্য {len(results)}টি ফলাফল পাওয়া গেছে:*", 
                parse_mode='Markdown',
                reply_markup=markup
            )
        else:
            bot.send_message(chat_id, f"❌ '{text}' এর জন্য কিছু পাওয়া যায়নি!")
            user_search[str(chat_id)] = False
        return
    
    if text == '📱 Get Number' or text == '/getnumber':
        if str(chat_id) not in user_country:
            bot.send_message(chat_id, "❌ আগে 🔍 Search Country দিয়ে দেশ সিলেক্ট করুন!")
            return
        
        # স্টপ থ্রেড ফ্ল্যাগ রিসেট করুন
        if str(chat_id) in running_threads:
            running_threads[str(chat_id)]['stop_flag'] = False
        
        # নাম্বার জেনারেশন শুরু করুন
        start_getting_numbers(message)
    
    elif text == '🛑 Stop & Show Numbers':
        stop_and_show_numbers(message)
    
    elif text == '💰 Balance' or text == '/balance':
        check_balance(message)
    
    elif text == '📊 Status' or text == '/status':
        show_status(message)
    
    elif text == '🗑️ Clear All' or text == '/clear':
        clear_all(message)
    
    elif text == 'ℹ️ Help' or text == '/help':
        show_help(message)
    
    elif text == '📜 Active Numbers':
        show_active_numbers(message)
    
    elif text == '🔢 Set Serial':
        set_serial_prompt(message)
    
    else:
        bot.send_message(chat_id, "❓ বাটন ব্যবহার করুন:", reply_markup=get_main_keyboard())

# ============= কলব্যাক =============
@bot.callback_query_handler(func=lambda call: True)
def handle_inline_callback(call):
    chat_id = call.message.chat.id
    
    if not is_user_allowed(call.from_user.id):
        bot.answer_callback_query(call.id, "⛔ আপনি অনুমোদিত নন!")
        return
    
    if call.data.startswith('country_'):
        parts = call.data.split('_')
        serial = parts[1]
        cuy = parts[2]
        country_name = "Unknown"
        for c in COUNTRIES:
            if c['serial'] == serial:
                country_name = c['name']
                break
        user_country[str(chat_id)] = {'serial': serial, 'cuy': cuy, 'name': country_name}
        bot.answer_callback_query(call.id, f"✅ {country_name} সিলেক্ট করা হয়েছে!")
        try:
            bot.delete_message(chat_id, call.message.message_id)
        except:
            pass
        bot.send_message(chat_id, 
            f"✅ *কান্ট্রি সিলেক্ট করা হয়েছে!*\n\n"
            f"🌍 {country_name}\n"
            f"📌 প্রোজেক্ট: `{DEFAULT_PID}`\n"
            f"🔢 সিরিয়াল: {format_serials_display(get_user_serials(chat_id))}", 
            parse_mode='Markdown',
            reply_markup=get_main_keyboard()
        )
    
    elif call.data == 'add_serials':
        bot.answer_callback_query(call.id, "সিরিয়াল টাইপ করুন")
        bot.send_message(chat_id,
            "📝 *সিরিয়াল লিখুন:*\n\n"
            "একাধিক সিরিয়াল কমা দিয়ে আলাদা করুন\n"
            "যেমন: `93,91,96`\n"
            "ডিফল্ট (সব): `2`",
            parse_mode='Markdown'
        )
        user_states[str(chat_id)] = 'waiting_serial'
    
    elif call.data == 'reset_serials':
        if str(chat_id) in user_serials:
            del user_serials[str(chat_id)]
        bot.answer_callback_query(call.id, "সিরিয়াল রিসেট!")
        try:
            bot.delete_message(chat_id, call.message.message_id)
        except:
            pass
        bot.send_message(chat_id,
            "🔄 *সিরিয়াল রিসেট করা হয়েছে!*\n\n"
            f"📌 এখন সব সিরিয়ালের নাম্বার আসবে (ডিফল্ট: {DEFAULT_SERIAL})",
            parse_mode='Markdown',
            reply_markup=get_main_keyboard()
        )
    
    elif call.data == 'view_serials':
        serials = get_user_serials(chat_id)
        bot.answer_callback_query(call.id, f"সিরিয়াল: {format_serials_display(serials)}")
        bot.send_message(chat_id,
            f"📋 *বর্তমান সিরিয়াল:* {format_serials_display(serials)}",
            parse_mode='Markdown'
        )
    
    elif call.data == 'cancel':
        bot.answer_callback_query(call.id, "বাতিল!")
        try:
            bot.delete_message(chat_id, call.message.message_id)
        except:
            pass
        user_states[str(chat_id)] = None
        user_search[str(chat_id)] = False
        bot.send_message(chat_id, "✅ বাতিল!", reply_markup=get_main_keyboard())
    
    elif call.data.startswith('check_'):
        phone = call.data.replace('check_', '')
        show_number_details(chat_id, phone)
    
    elif call.data == 'all_status':
        show_all_status(chat_id)
    
    elif call.data == 'clear_all':
        if str(chat_id) in user_data:
            for num_data in user_data[str(chat_id)]['numbers']:
                thread_key = f"{chat_id}_{num_data['phone']}"
                if thread_key in monitoring_threads:
                    del monitoring_threads[thread_key]
            del user_data[str(chat_id)]
        bot.answer_callback_query(call.id, "ক্লিয়ার!")
        try:
            bot.delete_message(chat_id, call.message.message_id)
        except:
            pass
        bot.send_message(chat_id, "✅ ক্লিয়ার!", reply_markup=get_main_keyboard())

# ============= স্টার্ট =============
@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    
    if not is_user_allowed(message.from_user.id):
        bot.send_message(chat_id, "⛔ আপনি এই বট ব্যবহার করার অনুমতি পাননি!")
        return
    
    if str(chat_id) not in user_country:
        user_country[str(chat_id)] = {'serial': '56', 'cuy': 'bd', 'name': 'Bangladesh'}
    
    try:
        params = {'name': USERNAME, 'ApiKey': API_KEY}
        data = call_api('getUserInfo', params)
        balance = data.get('data', {}).get('score', 'N/A')
    except:
        balance = 'N/A'
    
    bot.send_message(chat_id, 
        f"🌟 *ডুরিয়ান আরসিএস বটে স্বাগতম!*\n\n"
        f"✅ *একাউন্ট:* {USERNAME}\n"
        f"💰 *ব্যালেন্স:* {balance}\n"
        f"🌍 *বর্তমান দেশ:* {user_country[str(chat_id)]['name']}\n"
        f"📌 *প্রোজেক্ট:* `{DEFAULT_PID}`\n"
        f"🔢 *সিরিয়াল:* {format_serials_display(get_user_serials(chat_id))}\n"
        f"💰 *পয়েন্ট খরচ:* ১০০\n"
        f"⏳ *OTP অটো রিসিভ সক্রিয়*\n"
        f"📋 *মোট {len(COUNTRIES)}টি দেশ উপলব্ধ*\n\n"
        f"👤 *আপনার আইডি:* `{message.from_user.id}`\n\n"
        f"👇 *নিচের বাটন ব্যবহার করুন*", 
        parse_mode='Markdown', 
        reply_markup=get_main_keyboard()
    )

# ============= নাম্বার জেনারেশন (এনিমেটেড) =============
def start_getting_numbers(message):
    chat_id = message.chat.id
    user = message.from_user
    
    # আগের থ্রেড থাকলে স্টপ করুন
    if str(chat_id) in running_threads:
        running_threads[str(chat_id)]['stop_flag'] = True
        time.sleep(1)
    
    # নতুন থ্রেড শুরু করুন
    running_threads[str(chat_id)] = {
        'stop_flag': False,
        'thread': threading.Thread(target=generate_numbers_animated, args=(chat_id, user), daemon=True)
    }
    running_threads[str(chat_id)]['thread'].start()
    
    serials = get_user_serials(chat_id)
    bot.send_message(chat_id, 
        f"🔄 *নাম্বার জেনারেশন শুরু হয়েছে!*\n\n"
        f"🌍 দেশ: {user_country[str(chat_id)]['name']}\n"
        f"📌 প্রোজেক্ট: `{DEFAULT_PID}`\n"
        f"🔢 সিরিয়াল: {format_serials_display(serials)}\n"
        f"⏳ নাম্বার আসতে থাকবে...\n\n"
        f"🛑 *স্টপ করতে 'Stop & Show Numbers' বাটন ক্লিক করুন*",
        parse_mode='Markdown'
    )

def stop_and_show_numbers(message):
    chat_id = message.chat.id
    
    if str(chat_id) in running_threads:
        running_threads[str(chat_id)]['stop_flag'] = True
        
        # সব নাম্বার একসাথে দেখান
        chat_id_str = str(chat_id)
        if chat_id_str in user_data and user_data[chat_id_str]['numbers']:
            numbers = user_data[chat_id_str]['numbers']
            total = len(numbers)
            
            # নাম্বার লিস্ট তৈরি
            number_list = []
            for i, num_data in enumerate(numbers, 1):
                number_list.append(f"{i}. {num_data['phone']}")
            
            numbers_text = "\n".join(number_list)
            
            # কপি করার জন্য ফরম্যাট
            copy_text = "\n".join([num['phone'] for num in numbers])
            
            bot.send_message(chat_id,
                f"🛑 *নাম্বার জেনারেশন বন্ধ!*\n\n"
                f"📊 *মোট নাম্বার:* {total}টি\n"
                f"🌍 দেশ: {user_country[str(chat_id)]['name']}\n"
                f"📌 প্রোজেক্ট: `{DEFAULT_PID}`\n\n"
                f"📱 *সব নাম্বার:*\n{numbers_text}\n\n"
                f"📋 *কপি করার জন্য:*\n`{copy_text}`",
                parse_mode='Markdown'
            )
        else:
            bot.send_message(chat_id, "📭 কোনো নাম্বার পাওয়া যায়নি!")
    else:
        bot.send_message(chat_id, "❌ কোনো নাম্বার জেনারেশন চলছে না!")

def generate_numbers_animated(chat_id, user):
    """নাম্বার জেনারেট করতে থাকবে যতক্ষণ না স্টপ করা হয়"""
    try:
        country = user_country.get(str(chat_id), {'serial': '56', 'cuy': 'bd', 'name': 'Bangladesh'})
        user_identifier = f"@{user.username}" if user.username else user.first_name
        total_numbers = 0
        serials = get_user_serials(chat_id)
        
        # স্ট্যাটাস মেসেজ
        status_msg = bot.send_message(chat_id, 
            f"⏳ *নাম্বার সংগ্রহ করা হচ্ছে...*\n"
            f"🌍 দেশ: {country['name']}\n"
            f"📌 প্রোজেক্ট: `{DEFAULT_PID}`\n"
            f"🔢 সিরিয়াল: {format_serials_display(serials)}\n"
            f"📊 পেয়েছে: ০টি\n"
            f"🔄 চেষ্টা চলছে...\n\n"
            f"🛑 *স্টপ করতে 'Stop & Show Numbers' বাটন ক্লিক করুন*",
            parse_mode='Markdown'
        )
        
        serial_index = 0
        
        while not running_threads.get(str(chat_id), {}).get('stop_flag', True):
            try:
                # প্রতিটি সিরিয়াল দিয়ে চেষ্টা করুন
                current_serial = serials[serial_index % len(serials)]
                serial_index += 1
                
                params = {
                    'name': USERNAME,
                    'ApiKey': API_KEY,
                    'cuy': country['cuy'],
                    'pid': DEFAULT_PID,
                    'num': 1,
                    'noblack': 0,
                    'serial': current_serial,
                    'secret_key': 'null',
                    'vip': 'null'
                }
                data = call_api('getMobile', params)
                
                if data.get('code') == 200:
                    phone_number = data.get('data')
                    if phone_number and isinstance(phone_number, str):
                        total_numbers += 1
                        
                        chat_id_str = str(chat_id)
                        if chat_id_str not in user_data:
                            user_data[chat_id_str] = {'numbers': []}
                        
                        user_data[chat_id_str]['numbers'].append({
                            'phone': phone_number,
                            'timestamp': time.time(),
                            'pid': DEFAULT_PID,
                            'serial': current_serial,
                            'cuy': country['cuy'],
                            'country': country['name'],
                            'otp_received': False,
                            'otp_code': None,
                            'full_message': None,
                            'user': user_identifier
                        })
                        
                        start_monitoring(chat_id, phone_number, user_identifier)
                        
                        # নাম্বার দেখান
                        bot.send_message(chat_id, 
                            f"📱 `{phone_number}`\n"
                            f"✅ নাম্বার পেলাম! (মোট: {total_numbers}টি)\n"
                            f"🔢 সিরিয়াল: {current_serial}\n"
                            f"🔍 OTP মনিটরিং চলছে...",
                            parse_mode='Markdown'
                        )
                        
                        # স্ট্যাটাস আপডেট
                        try:
                            bot.edit_message_text(
                                f"⏳ *নাম্বার সংগ্রহ করা হচ্ছে...*\n"
                                f"🌍 দেশ: {country['name']}\n"
                                f"📌 প্রোজেক্ট: `{DEFAULT_PID}`\n"
                                f"🔢 সিরিয়াল: {format_serials_display(serials)}\n"
                                f"📊 পেয়েছে: {total_numbers}টি\n"
                                f"🔄 চেষ্টা চলছে...\n\n"
                                f"🛑 *স্টপ করতে 'Stop & Show Numbers' বাটন ক্লিক করুন*",
                                chat_id,
                                status_msg.message_id,
                                parse_mode='Markdown'
                            )
                        except:
                            pass
                        
                        time.sleep(1.5)
                    else:
                        time.sleep(1)
                else:
                    error_msg = data.get('msg', 'Unknown error')
                    if data.get('code') == 403:
                        bot.send_message(chat_id, "⚠️ ব্যালেন্স কম! রিচার্জ করুন।")
                        break
                    elif data.get('code') == 904:
                        bot.send_message(chat_id, f"⚠️ প্রোজেক্ট আইডি {DEFAULT_PID} সঠিক নয়!")
                        break
                    time.sleep(1)
                
            except Exception as e:
                print(f"❌ জেনারেশন এরর: {e}")
                time.sleep(1)
        
        # থ্রেড শেষে ক্লিনআপ
        if str(chat_id) in running_threads:
            del running_threads[str(chat_id)]
        
        # শেষ স্ট্যাটাস
        try:
            bot.edit_message_text(
                f"🛑 *নাম্বার জেনারেশন বন্ধ!*\n\n"
                f"🌍 দেশ: {country['name']}\n"
                f"📌 প্রোজেক্ট: `{DEFAULT_PID}`\n"
                f"📊 মোট নাম্বার: {total_numbers}টি\n"
                f"🔍 সব OTP মনিটরিং চলছে...",
                chat_id,
                status_msg.message_id,
                parse_mode='Markdown'
            )
        except:
            pass
        
        # সব নাম্বার একসাথে দেখান
        if total_numbers > 0:
            chat_id_str = str(chat_id)
            if chat_id_str in user_data and user_data[chat_id_str]['numbers']:
                numbers = user_data[chat_id_str]['numbers']
                number_list = []
                for i, num_data in enumerate(numbers, 1):
                    number_list.append(f"{i}. {num_data['phone']}")
                
                numbers_text = "\n".join(number_list)
                copy_text = "\n".join([num['phone'] for num in numbers])
                
                bot.send_message(chat_id,
                    f"📱 *সব নাম্বার একসাথে:*\n\n"
                    f"{numbers_text}\n\n"
                    f"📋 *কপি করার জন্য:*\n`{copy_text}`",
                    parse_mode='Markdown'
                )
            
            # অ্যাক্টিভ নাম্বার দেখান
            markup = types.InlineKeyboardMarkup(row_width=2)
            numbers = user_data.get(str(chat_id), {}).get('numbers', [])[-10:]
            for num_data in numbers:
                markup.add(types.InlineKeyboardButton(f"📱 {num_data['phone'][-4:]}", callback_data=f"check_{num_data['phone']}"))
            markup.add(types.InlineKeyboardButton("📊 সব স্ট্যাটাস", callback_data="all_status"))
            markup.add(types.InlineKeyboardButton("🗑️ ক্লিয়ার", callback_data="clear_all"))
            bot.send_message(chat_id, "👇 *ডিটেইলস:*", parse_mode='Markdown', reply_markup=markup)
        
    except Exception as e:
        bot.send_message(chat_id, f"❌ জেনারেশন থ্রেড ত্রুটি: {str(e)}")
        if str(chat_id) in running_threads:
            del running_threads[str(chat_id)]

# ============= OTP মনিটরিং (অটো রিসিভ) =============
def start_monitoring(chat_id, phone_number, user_identifier):
    thread_key = f"{chat_id}_{phone_number}"
    if thread_key in monitoring_threads and monitoring_threads[thread_key].is_alive():
        return
    
    print(f"🔍 OTP মনিটরিং স্টার্ট: {phone_number} ({user_identifier})")
    thread = threading.Thread(target=monitor_otp, args=(chat_id, phone_number, user_identifier), daemon=True)
    monitoring_threads[thread_key] = thread
    thread.start()
    print(f"✅ OTP মনিটরিং থ্রেড চালু: {phone_number}")

def monitor_otp(chat_id, phone_number, user_identifier):
    start_time = time.time()
    chat_id_str = str(chat_id)
    
    pid = DEFAULT_PID
    serial = "56"
    if chat_id_str in user_data:
        for num_data in user_data[chat_id_str]['numbers']:
            if num_data['phone'] == phone_number:
                pid = num_data.get('pid', DEFAULT_PID)
                serial = num_data.get('serial', '56')
                break
    
    print(f"👀 OTP মনিটরিং: {phone_number} (PID: {pid})")
    
    while time.time() - start_time < OTP_TIMEOUT:
        try:
            params = {
                'name': USERNAME,
                'ApiKey': API_KEY,
                'pn': phone_number,
                'pid': pid,
                'serial': 2
            }
            data = call_api('getMsg', params)
            
            if data.get('code') == 200:
                otp_code = data.get('data')
                if otp_code:
                    # OTP পাওয়া গেছে!
                    if chat_id_str in user_data:
                        for num_data in user_data[chat_id_str]['numbers']:
                            if num_data['phone'] == phone_number:
                                num_data['otp_received'] = True
                                num_data['otp_code'] = otp_code
                                num_data['full_message'] = otp_code
                                break
                    
                    # OTP মেসেজ তৈরি
                    otp_message = (
                        f"🔔 *OTP পাওয়া গেছে!*\n\n"
                        f"📱 নাম্বার: `{phone_number}`\n"
                        f"🔑 কোড: `{otp_code}`\n"
                        f"👤 ইউজার: {user_identifier}\n"
                        f"📌 প্রোজেক্ট: `{pid}`\n"
                        f"⏰ {datetime.now().strftime('%I:%M:%S %p')}\n\n"
                        f"✅ OTP সফলভাবে রিসিভ হয়েছে!"
                    )
                    
                    # ১. ইউজারের কাছে পাঠান
                    bot.send_message(chat_id, otp_message, parse_mode='Markdown')
                    
                    # ২. OTP গ্রুপে পাঠান
                    if GROUP_ID:
                        try:
                            bot.send_message(GROUP_ID, otp_message, parse_mode='Markdown')
                            print(f"📤 OTP গ্রুপে পাঠানো হয়েছে: {GROUP_ID}")
                        except Exception as e:
                            print(f"⚠️ গ্রুপে OTP পাঠাতে ব্যর্থ: {e}")
                    
                    print(f"✅ OTP পাওয়া গেছে: {phone_number} -> {otp_code} ({user_identifier})")
                    break
            
            time.sleep(OTP_CHECK_INTERVAL)
            
        except Exception as e:
            print(f"⚠️ OTP মনিটরিং এরর: {e}")
            time.sleep(OTP_CHECK_INTERVAL)
    
    # টাইমআউট হলে কিছুই করবেন না (মেসেজ আসবে না)
    thread_key = f"{chat_id}_{phone_number}"
    if thread_key in monitoring_threads:
        del monitoring_threads[thread_key]
    
    print(f"⏹️ OTP মনিটরিং বন্ধ: {phone_number}")

# ============= হেল্পার =============
def show_number_details(chat_id, phone):
    chat_id_str = str(chat_id)
    if chat_id_str in user_data:
        for num_data in user_data[chat_id_str]['numbers']:
            if num_data['phone'] == phone:
                status = "✅ OTP প্রাপ্ত" if num_data['otp_received'] else "⏳ অপেক্ষমান"
                otp = num_data['otp_code'] if num_data['otp_code'] else "N/A"
                remaining = int(OTP_TIMEOUT - (time.time() - num_data['timestamp']))
                user_info = num_data.get('user', 'Unknown')
                serial = num_data.get('serial', 'N/A')
                bot.send_message(chat_id, 
                    f"📱 `{phone}`\n"
                    f"স্ট্যাটাস: {status}\n"
                    f"OTP: `{otp}`\n"
                    f"👤 ইউজার: {user_info}\n"
                    f"🔢 সিরিয়াল: {serial}\n"
                    f"ভ্যালিডিটি: {remaining}s\n"
                    f"📌 প্রোজেক্ট: `{num_data.get('pid', DEFAULT_PID)}`", 
                    parse_mode='Markdown'
                )
                break

def show_all_status(chat_id):
    chat_id_str = str(chat_id)
    if chat_id_str in user_data:
        text = "📊 *স্ট্যাটাস:*\n\n"
        for num_data in user_data[chat_id_str]['numbers']:
            status = "✅ OTP প্রাপ্ত" if num_data['otp_received'] else "⏳ অপেক্ষমান"
            otp = num_data['otp_code'] if num_data['otp_code'] else "..."
            remaining = int(OTP_TIMEOUT - (time.time() - num_data['timestamp']))
            user_info = num_data.get('user', 'Unknown')
            serial = num_data.get('serial', 'N/A')
            text += f"{status} `{num_data['phone']}` → OTP: `{otp}` ({remaining}s) 🔢{serial} 👤 {user_info}\n"
        bot.send_message(chat_id, text, parse_mode='Markdown')

def show_active_numbers(message):
    chat_id = message.chat.id
    chat_id_str = str(chat_id)
    
    if chat_id_str in user_data and user_data[chat_id_str]['numbers']:
        text = "📱 *আপনার অ্যাক্টিভ নাম্বার:*\n\n"
        for i, num_data in enumerate(user_data[chat_id_str]['numbers'], 1):
            remaining = int(OTP_TIMEOUT - (time.time() - num_data['timestamp']))
            if remaining > 0:
                status = "✅ OTP পেয়েছে" if num_data['otp_received'] else "⏳ অপেক্ষমান"
                user_info = num_data.get('user', 'Unknown')
                serial = num_data.get('serial', 'N/A')
                text += f"{i}. `{num_data['phone']}`\n   → {status}\n   → 👤 {user_info}\n   → 🔢{serial}\n   → {remaining}সেকেন্ড বাকি\n\n"
            else:
                text += f"{i}. `{num_data['phone']}` ⏰ এক্সপায়ার্ড\n\n"
        
        if len(text) > 4000:
            text = text[:4000] + "\n...(বাকি অংশ কাটা হয়েছে)"
        bot.send_message(chat_id, text, parse_mode='Markdown')
    else:
        bot.send_message(chat_id, "📭 কোনো অ্যাক্টিভ নাম্বার নেই!")

def show_status(message):
    chat_id = message.chat.id
    chat_id_str = str(chat_id)
    if chat_id_str in user_data and user_data[chat_id_str]['numbers']:
        total = len(user_data[chat_id_str]['numbers'])
        received = sum(1 for n in user_data[chat_id_str]['numbers'] if n['otp_received'])
        bot.send_message(chat_id, f"📊 মোট: {total}, OTP প্রাপ্ত: {received}")
    else:
        bot.send_message(chat_id, "📭 কোনো নাম্বার নেই!")

def clear_all(message):
    chat_id = message.chat.id
    chat_id_str = str(chat_id)
    if chat_id_str in user_data:
        for num_data in user_data[chat_id_str]['numbers']:
            thread_key = f"{chat_id}_{num_data['phone']}"
            if thread_key in monitoring_threads:
                del monitoring_threads[thread_key]
        del user_data[chat_id_str]
        bot.send_message(chat_id, "✅ ক্লিয়ার!", reply_markup=get_main_keyboard())

def check_balance(message):
    chat_id = message.chat.id
    try:
        params = {'name': USERNAME, 'ApiKey': API_KEY}
        data = call_api('getUserInfo', params)
        print(f"📊 {data}")
        
        if data.get('code') == 200:
            balance = data.get('data', {}).get('score', 'N/A')
            bot.send_message(chat_id, 
                f"💰 *ব্যালেন্স: {balance}*\n\n"
                f"👤 *একাউন্ট:* {USERNAME}\n"
                f"📌 *প্রোজেক্ট:* `{DEFAULT_PID}`\n"
                f"💰 *পয়েন্ট খরচ:* ১০০", 
                parse_mode='Markdown'
            )
        else:
            bot.send_message(chat_id, f"❌ {data.get('msg', 'Error')}")
    except Exception as e:
        bot.send_message(chat_id, f"❌ {str(e)}")

def show_help(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    is_allowed = "✅ অনুমোদিত" if is_user_allowed(user_id) else "⛔ অনুমোদিত নয়"
    
    bot.send_message(chat_id, 
        f"📚 *হেল্প:*\n\n"
        f"👤 *আপনার স্ট্যাটাস:* {is_allowed}\n"
        f"🆔 *আপনার আইডি:* `{user_id}`\n\n"
        f"🔍 **Search Country** - নাম/শর্টকাট দিয়ে দেশ খুঁজুন\n"
        f"   যেমন: `bd`, `bangladesh`, `us`, `india`, `uk`\n"
        f"🔢 **Set Serial** - সিরিয়াল সেট করুন (একাধিক সিরিয়াল কমা দিয়ে)\n"
        f"   যেমন: `/setserial 93,91,96`\n"
        f"📱 **Get Number** - নাম্বার নেওয়া শুরু করুন (অটোমেটিক)\n"
        f"   ⏳ *স্টপ না করা পর্যন্ত নাম্বার আসতে থাকবে*\n"
        f"🛑 **Stop & Show Numbers** - নাম্বার জেনারেশন বন্ধ + সব নাম্বার দেখান\n"
        f"💰 **Balance** - ব্যালেন্স চেক\n"
        f"📊 **Status** - স্ট্যাটাস দেখুন\n"
        f"📜 **Active Numbers** - অ্যাক্টিভ নাম্বার দেখুন\n"
        f"🗑️ **Clear All** - সব ক্লিয়ার\n\n"
        f"📌 *প্রোজেক্ট আইডি:* `{DEFAULT_PID}`\n"
        f"💰 *পয়েন্ট খরচ:* ১০০\n"
        f"⏱️ *OTP চেক ইন্টারভাল:* {OTP_CHECK_INTERVAL} সেকেন্ড\n"
        f"🌍 *মোট {len(COUNTRIES)}টি দেশ উপলব্ধ*\n\n"
        f"✨ *অটো OTP:* OTP আসলেই নিজে থেকেই চলে আসবে!\n"
        f"📢 *শুধু OTP গ্রুপে পাঠানো হবে*\n"
        f"⏰ *টাইমআউট মেসেজ বন্ধ করা হয়েছে*", 
        parse_mode='Markdown'
    )

# ============= চালান =============
if __name__ == "__main__":
    print("=" * 50)
    print("🤖 ডুরিয়ান আরসিএস বট চালু হচ্ছে...")
    print(f"👤 ইউজারনেম: {USERNAME}")
    print(f"📌 প্রোজেক্ট আইডি: {DEFAULT_PID}")
    print(f"💰 পয়েন্ট খরচ: ১০০")
    print(f"⏱️ OTP চেক ইন্টারভাল: {OTP_CHECK_INTERVAL} সেকেন্ড")
    print(f"📢 OTP গ্রুপ: {GROUP_ID}")
    print(f"👥 অনুমোদিত ইউজার: {len(ALLOWED_USERS) if ALLOWED_USERS else 'সবাই'}")
    print(f"🌍 সাপোর্টেড দেশ: {len(COUNTRIES)}টি")
    print(f"🔢 ডিফল্ট সিরিয়াল: {DEFAULT_SERIAL} (সব)")
    print("=" * 50)
    print("✅ শুধু OTP গ্রুপে পাঠানো হবে!")
    print("⏰ টাইমআউট মেসেজ বন্ধ করা হয়েছে!")
    print("📱 টেলিগ্রামে /start দিন")
    print("=" * 50)
    
    while True:
        try:
            bot.polling(none_stop=True, interval=1)
        except Exception as e:
            print(f"❌ {e}")
            time.sleep(5)
