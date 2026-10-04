DropdownButtonHideUnderline(
    child: DropdownButton<String>(
        value: metricValue,
        isExpanded: true,
        borderRadius: BorderRadius.circular(12),
        style: theme.textTheme.headlineSmall?.copyWith(
            fontWeight: FontWeight.w700,
            color: colorScheme.onSurface,
        ),
        items: [
            DropdownMenuItem(
                value: db.foods.calories.name,
                child: Text(context.l10n.calories),
            ),
             DropdownMenuItem(
                value: 'body-weight',
                child: Text(context.l10n.bodyWeight),
            ),
            ...filteredFields.map(
                (field) => DropdownMenuItem(
                    value: field,
                    child: Text(
                        localizedFoodFieldLabel(context.l10n, field),
                    ),
                ),
            ),
        ],
        onChanged: (value) {
            if (value == null) return;
            setState(() => metric = value);
            db.settings.update().write(
                SettingsCompanion(lastGraph: Value(metric)),
            );
        },
    ),
)