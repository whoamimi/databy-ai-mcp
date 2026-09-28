"""metadata = SessionForm(
    business_domain=BusinessDomain.TRANSACTIONS,
    objective="Clean transaction data",
    clean_state=CleanState.MESS,
)

session = create_session(metadata)

session = attach_file(
    session,
    filename="transactions.csv",
    content_type="text/csv",
    size_bytes=125_000,
    path=Path("data/transactions.csv"),
)

print(session.model_dump_json(indent=2))
"""
