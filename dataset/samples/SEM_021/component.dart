import 'package:flutter/material.dart';

/// A Text where parts between "**" are in bold
class TextWithBoldParts extends StatelessWidget {
  const TextWithBoldParts({
    required this.text,
    this.textStyle,
    this.boldTextStyle,
    this.textAlign,
    this.overflow,
    this.maxLines,
    super.key,
  });

  final String text;
  final TextStyle? textStyle;
  final TextStyle? boldTextStyle;
  final TextAlign? textAlign;
  final TextOverflow? overflow;
  final int? maxLines;

  @override
  Widget build(BuildContext context) {
    final TextStyle defaultTextStyle = textStyle ?? const TextStyle();
    return Semantics(
      value: text.replaceAll(r'**', '').replaceAll('\n', ' '),
      excludeSemantics: true,
      child: RichText(
        textScaler: MediaQuery.textScalerOf(context),
        text: TextSpan(
          style: DefaultTextStyle.of(context).style,
          children:
              _getPartsBetweenSymbol(
                    text: text,
                    symbol: r'\*\*',
                    symbolLength: 2,
                    defaultStyle: defaultTextStyle,
                    highlightedStyle:
                        boldTextStyle ??
                        const TextStyle(fontWeight: FontWeight.bold),
                  )
                  .map(((String, TextStyle?) part) {
                    return TextSpan(
                      text: part.$1,
                      style: defaultTextStyle.merge(part.$2),
                      semanticsLabel: '-',
                    );
                  })
                  .toList(growable: false),
        ),
        textAlign: textAlign ?? TextAlign.start,
        overflow: overflow ?? TextOverflow.clip,
        maxLines: maxLines,
      ),
    );
  }
}

List<(String, TextStyle?)> _getPartsBetweenSymbol({
  required String text,
  required String symbol,
  required int symbolLength,
  required TextStyle? defaultStyle,
  required TextStyle? highlightedStyle,
}) {
  text = text.replaceAll(r'\n', '\n');

  final Iterable<RegExpMatch> highlightedParts = RegExp(
    '$symbol[^$symbol]+$symbol',
  ).allMatches(text);

  final List<(String, TextStyle?)> parts = <(String, TextStyle?)>[];

  if (highlightedParts.isEmpty) {
    parts.add((text, defaultStyle));
  } else {
    parts.add((
      text.substring(0, highlightedParts.first.start),
      defaultStyle,
    ));
    for (int i = 0; i != highlightedParts.length; i++) {
      final RegExpMatch subPart = highlightedParts.elementAt(i);

      parts.add((
        text.substring(
          subPart.start + symbolLength,
          subPart.end - symbolLength,
        ),
        highlightedStyle,
      ));

      if (i < highlightedParts.length - 1) {
        parts.add((
          text.substring(
            subPart.end,
            highlightedParts.elementAt(i + 1).start,
          ),
          defaultStyle,
        ));
      } else if (subPart.end < text.length) {
        parts.add((text.substring(subPart.end, text.length), defaultStyle));
      }
    }
  }
  return parts;
}
