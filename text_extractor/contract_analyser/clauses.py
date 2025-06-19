# Clause definitions: ideal phrasing and phrases to flag
CLAUSES = {
    "Break Clause": {
        "positive": ["tenant may terminate the tenancy after six months", "either party may end with notice"],
        "negative": ["tenant must remain for full term", "no early termination"]
    },
    "Repairs and Maintenance": {
        "positive": ["landlord responsible for repairs", "repair boiler", "maintain structure"],
        "negative": ["tenant responsible for repairs", "tenant to maintain"]
    },
    "Rent Increases": {
        "positive": ["rent fixed for 12 months", "linked to rpi"],
        "negative": ["landlord may increase rent at any time"]
    },
    "Deposit Handling": {
        "positive": ["protected in a government scheme", "tds", "dps", "mydeposits"],
        "negative": ["non-refundable deposit", "no deposit protection"]
    },
    "Access and Privacy": {
        "positive": ["landlord must give 24 hours notice", "written notice before entry"],
        "negative": ["landlord may enter at any time", "no notice required"]
    },
    "Prohibited Fees": {
        "positive": ["no admin fees", "tenant fees act compliant"],
        "negative": ["check-out fee", "admin charge", "inventory fee"]
    },
    "Subletting and Guests": {
        "positive": ["subletting allowed with consent", "guests permitted"],
        "negative": ["subletting prohibited", "guests not allowed"]
    }
}
