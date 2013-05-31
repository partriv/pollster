from pollster.conf import settings_local
import pollster.settings

SITE_NAME = "Pollstruck"


CHART_TYPE_PIE = 'pie'
CHART_TYPE_BAR = 'bar'
CHART_TYPE_HBAR = 'hbar'
CHART_TYPES_WHITE_LIST = [CHART_TYPE_PIE, CHART_TYPE_BAR, CHART_TYPE_HBAR]
DEFAULT_CHART_TYPE = CHART_TYPE_PIE

################################
# Home and View thumbnail sizes
#################################
THUMB_WIDTH_TINY = 16
THUMB_HEIGHT_TINY = 16

THUMB_WIDTH_SM = 24
THUMB_HEIGHT_SM = 24

THUMB_WIDTH_MED = 64
THUMB_HEIGHT_MED = 64

THUMB_WIDTH_LG = 128
THUMB_HEIGHT_LG = 128

# urls
ERROR_PAGE = settings_local.HOST_NAME + 'error/'

## POLL ANSWER STYLE TYPES
PREDEFINED_ANSWERS = 1

#########################
# POLL CREATOR CONSTS
#########################
MIN_ANSWERS_FOR_ACTIVE_POLL = 2
MIN_TAGS_FOR_ACTIVE_POLL = 0
MAX_PICS_PER_POLL = 5

IMAGES_WHITE_LIST = [".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tif"]
OTHER_FILES_WHITE_LIST = [".txt", ".doc", ".xls", ".ppt", ".mp3", ".pdf"]

#########################
# MAGIC NUMBERS
#########################

POLL_LISTER_RPP = 12

POLL_RESULTS_MAGIC_THRESH = 10
POLL_ANSWERS_MAGIC_THRESH = POLL_RESULTS_MAGIC_THRESH + 3 
# subtract one for the tricky offset math 
# make it true magic thresh hold start counting at index 1
POLL_RESULTS_MAGIC_THRESH -= 1

POLL_ANSWER_LIMIT = 20

# in days
POLL_ACTIVITY_WINDOW = 20

POLL_VOTES_BEFORE_PERMANENTLY_ACTIVE = 5

#####################
# LOGIN SHIT?
######################
ERROR_LOGGED_IN = 1
ERROR_ENGLISH = {
    ERROR_LOGGED_IN : 'You are already logged in.',

}

######################
# search consts
######################
SORT_TYPE_COMMENTS = "comments"
SORT_TYPE_DATE = "date"
SORT_TYPE_VOTES = "votes"

########################
# facebook constants
########################

######################
# Profile constants
######################

PROFILE_NO_ANSWER = 0
PROFILE_INCOME_25K = 1
PROFILE_INCOME_50K = 2
PROFILE_INCOME_75K = 3
PROFILE_INCOME_100K = 4
PROFILE_INCOME_125K = 5
PROFILE_INCOME_150K = 6
PROFILE_INCOME_175K = 7
PROFILE_INCOME_200K = 8
PROFILE_INCOME_200K_PLUS = 9

PROFILE_INCOME_ENGLISH = {
    PROFILE_NO_ANSWER : 'Choose an answer',
    PROFILE_INCOME_25K : 'Less than $25,000',
    PROFILE_INCOME_50K : '$25,001 to $50,000',
    PROFILE_INCOME_75K : '$50,001 to $75,000',
    PROFILE_INCOME_100K : '$75,001 to $100,000',
    PROFILE_INCOME_125K : '$100,001 to $125,000',
    PROFILE_INCOME_150K : '$125,001 to $150,000',
    PROFILE_INCOME_175K : '$150,001 to $175,000',
    PROFILE_INCOME_200K : '$175,001 to $200,000',
    PROFILE_INCOME_200K_PLUS : '$200,001 or More',
}


PROFILE_SEX_MALE = 0
PROFILE_SEX_FEMALE = 1

PROFILE_SEX_ENGLISH = {
    PROFILE_NO_ANSWER : 'Choose an answer',
    PROFILE_SEX_MALE : 'Male',
    PROFILE_SEX_FEMALE : 'Female',
}

PROFILE_SEXES_ENGLISH = {
    PROFILE_NO_ANSWER : 'Choose an answer',
    1 : 'Straight',
    2 : 'Gay',
    3 : 'Bisexual',
}

PROFILE_UNITED_STATES = 226
PROFILE_COUNTRY_CODES = {
    PROFILE_NO_ANSWER : 'Choose an answer',
    1 : 'Afghanistan',
    2 : 'Albania',
    3 : 'Algeria',
    4 : 'American Samoa',
    5 : 'Andorra',
    6 : 'Angola',
    7 : 'Anguilla',
    8 : 'Antarctica',
    9 : 'Antigua and Barbuda',
    10 : 'Argentina',
    11 : 'Armenia',
    12 : 'Aruba',
    13 : 'Australia',
    14 : 'Austria',
    15 : 'Azerbaijan',
    16 : 'Bahamas',
    17 : 'Bahrain',
    18 : 'Bangladesh',
    19 : 'Barbados',
    20 : 'Belarus',
    21 : 'Belgium',
    22 : 'Belize',
    23 : 'Benin',
    24 : 'Bermuda',
    25 : 'Bhutan',
    26 : 'Bolivia',
    27 : 'Bosnia and Herzegovina',
    28 : 'Botswana',
    29 : 'Bouvet Island',
    30 : 'Brazil',
    31 : 'British Indian Ocean Territory',
    32 : 'Brunei Darussalam',
    33 : 'Bulgaria',
    34 : 'Burkina Faso',
    35 : 'Burundi',
    36 : 'Cambodia',
    37 : 'Cameroon',
    38 : 'Canada',
    39 : 'Cape Verde',
    40 : 'Cayman Islands',
    41 : 'Central African Republic',
    42 : 'Chad',
    43 : 'Chile',
    44 : 'China',
    45 : 'Christmas Island',
    46 : 'Cocos (Keeling) Islands',
    47 : 'Colombia',
    48 : 'Comoros',
    49 : 'Congo',
    50 : 'Congo, the Democratic Republic of the',
    51 : 'Cook Islands',
    52 : 'Costa Rica',
    53 : 'Cote D&#39;Ivoire',
    54 : 'Croatia',
    55 : 'Cuba',
    56 : 'Cyprus',
    57 : 'Czech Republic',
    58 : 'Denmark',
    59 : 'Djibouti',
    60 : 'Dominica',
    61 : 'Dominican Republic',
    62 : 'Ecuador',
    63 : 'Egypt',
    64 : 'El Salvador',
    65 : 'Equatorial Guinea',
    66 : 'Eritrea',
    67 : 'Estonia',
    68 : 'Ethiopia',
    69 : 'Falkland Islands (Malvinas)',
    70 : 'Faroe Islands',
    71 : 'Fiji',
    72 : 'Finland',
    73 : 'France',
    74 : 'French Guiana',
    75 : 'French Polynesia',
    76 : 'French Southern Territories',
    77 : 'Gabon',
    78 : 'Gambia',
    79 : 'Georgia',
    80 : 'Germany',
    81 : 'Ghana',
    82 : 'Gibraltar',
    83 : 'Greece',
    84 : 'Greenland',
    85 : 'Grenada',
    86 : 'Guadeloupe',
    87 : 'Guam',
    88 : 'Guatemala',
    89 : 'Guinea',
    90 : 'Guinea-Bissau',
    91 : 'Guyana',
    92 : 'Haiti',
    93 : 'Heard Island and Mcdonald Islands',
    94 : 'Holy See (Vatican City State)',
    95 : 'Honduras',
    96 : 'Hong Kong',
    97 : 'Hungary',
    98 : 'Iceland',
    99 : 'India',
    100 : 'Indonesia',
    101 : 'Iran, Islamic Republic of',
    102 : 'Iraq',
    103 : 'Ireland',
    104 : 'Israel',
    105 : 'Italy',
    106 : 'Jamaica',
    107 : 'Japan',
    108 : 'Jordan',
    109 : 'Kazakhstan',
    110 : 'Kenya',
    111 : 'Kiribati',
    112 : 'Korea, Democratic People&#39;s Republic of',
    113 : 'Korea, Republic of',
    114 : 'Kuwait',
    115 : 'Kyrgyzstan',
    116 : 'Lao People&#39;s Democratic Republic',
    117 : 'Latvia',
    118 : 'Lebanon',
    119 : 'Lesotho',
    120 : 'Liberia',
    121 : 'Libyan Arab Jamahiriya',
    122 : 'Liechtenstein',
    123 : 'Lithuania',
    124 : 'Luxembourg',
    125 : 'Macao',
    126 : 'Macedonia, the Former Yugoslav Republic of',
    127 : 'Madagascar',
    128 : 'Malawi',
    129 : 'Malaysia',
    130 : 'Maldives',
    131 : 'Mali',
    132 : 'Malta',
    133 : 'Marshall Islands',
    134 : 'Martinique',
    135 : 'Mauritania',
    136 : 'Mauritius',
    137 : 'Mayotte',
    138 : 'Mexico',
    139 : 'Micronesia, Federated States of',
    140 : 'Moldova, Republic of',
    141 : 'Monaco',
    142 : 'Mongolia',
    143 : 'Montserrat',
    144 : 'Morocco',
    145 : 'Mozambique',
    146 : 'Myanmar',
    147 : 'Namibia',
    148 : 'Nauru',
    149 : 'Nepal',
    150 : 'Netherlands',
    151 : 'Netherlands Antilles',
    152 : 'New Caledonia',
    153 : 'New Zealand',
    154 : 'Nicaragua',
    155 : 'Niger',
    156 : 'Nigeria',
    157 : 'Niue',
    158 : 'Norfolk Island',
    159 : 'Northern Mariana Islands',
    160 : 'Norway',
    161 : 'Oman',
    162 : 'Pakistan',
    163 : 'Palau',
    164 : 'Palestinian Territory, Occupied',
    165 : 'Panama',
    166 : 'Papua New Guinea',
    167 : 'Paraguay',
    168 : 'Peru',
    169 : 'Philippines',
    170 : 'Pitcairn',
    171 : 'Poland',
    172 : 'Portugal',
    173 : 'Puerto Rico',
    174 : 'Qatar',
    175 : 'Reunion',
    176 : 'Romania',
    177 : 'Russian Federation',
    178 : 'Rwanda',
    179 : 'Saint Helena',
    180 : 'Saint Kitts and Nevis',
    181 : 'Saint Lucia',
    182 : 'Saint Pierre and Miquelon',
    183 : 'Saint Vincent and the Grenadines',
    184 : 'Samoa',
    185 : 'San Marino',
    186 : 'Sao Tome and Principe',
    187 : 'Saudi Arabia',
    188 : 'Senegal',
    189 : 'Serbia and Montenegro',
    190 : 'Seychelles',
    191 : 'Sierra Leone',
    192 : 'Singapore',
    193 : 'Slovakia',
    194 : 'Slovenia',
    195 : 'Solomon Islands',
    196 : 'Somalia',
    197 : 'South Africa',
    198 : 'South Georgia and the South Sandwich Islands',
    199 : 'Spain',
    200 : 'Sri Lanka',
    201 : 'Sudan',
    202 : 'Suriname',
    203 : 'Svalbard and Jan Mayen',
    204 : 'Swaziland',
    205 : 'Sweden',
    206 : 'Switzerland',
    207 : 'Syrian Arab Republic',
    208 : 'Taiwan, Province of China',
    209 : 'Tajikistan',
    210 : 'Tanzania, United Republic of',
    211 : 'Thailand',
    212 : 'Timor-Leste',
    213 : 'Togo',
    214 : 'Tokelau',
    215 : 'Tonga',
    216 : 'Trinidad and Tobago',
    217 : 'Tunisia',
    218 : 'Turkey',
    219 : 'Turkmenistan',
    220 : 'Turks and Caicos Islands',
    221 : 'Tuvalu',
    222 : 'Uganda',
    223 : 'Ukraine',
    224 : 'United Arab Emirates',
    225 : 'United Kingdom',
    PROFILE_UNITED_STATES : 'United States',
    227 : 'United States Minor Outlying Islands',
    228 : 'Uruguay',
    229 : 'Uzbekistan',
    230 : 'Vanuatu',
    231 : 'Venezuela',
    232 : 'Viet Nam',
    233 : 'Virgin Islands, British',
    234 : 'Virgin Islands, U.S.',
    235 : 'Wallis and Futuna',
    236 : 'Western Sahara',
    237 : 'Yemen',
    238 : 'Zambia',
    239 : 'Zimbabwe',
}

PROFILE_ETHNICITY = {
    PROFILE_NO_ANSWER : 'Choose an answer',
    1 : 'Alaska Native',
    2 : 'African American',
    3 : 'American Indian',
    4 : 'Asian',
    5 : 'Native Hawaiian',
    6 : 'Pacific Islander',
    7 : 'Caucasian',
    8 : 'Other',
}

PROFILE_RELATIONSHIP_STATUS = {
    PROFILE_NO_ANSWER : 'Choose an answer',
    1 : 'Single',
    2 : 'In a Relationship',
    3 : 'Engaged',
    4 : 'Married',
    5 : 'It\'s Complicated',
    6 : 'In an Open Relationship',
}

PROFILE_IM_SERVICES = {
    PROFILE_NO_ANSWER : 'Choose an answer',
    1 : 'AIM',
    2 : 'Google Talk',
    3 : 'Skype',
    4 : 'Windows Live',
    5 : 'Yahoo',
    6 : 'ICQ',
}
