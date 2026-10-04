Container(
    alignment: Alignment.bottomRight,
    padding: EdgeInsets.all(20),
    child: ElevatedButton(
        onPressed: () {
            Navigator.pop(context, allIngredientSelected);
        },
        child: Text(AppLocalizations.of(context)!.add),
    )
)