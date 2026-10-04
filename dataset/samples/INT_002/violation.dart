DropdownButton<String>(
    value: metricValue,
    items: [
        DropdownMenuItem(
            value: 'calories',
            child: Text('Cal'),
        ),
        DropdownMenuItem(
            value: 'body-weight',
            child: Text('Wt'),
        ),
    ],
    onChanged: (value) => setState(() => metric = value),
)