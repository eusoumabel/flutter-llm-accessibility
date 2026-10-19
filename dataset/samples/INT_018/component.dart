import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';

class KeypadKeyButton extends StatefulWidget {
  const KeypadKeyButton({
    super.key,
    required this.text,
    required this.subtext,
    required this.onKeyPressed,
  });

  static const _subextPadding = EdgeInsets.symmetric(horizontal: 8);

  /// Minimum alpha value applied when deriving subtext color.
  static const double _minAlphaValue = 0.2;

  /// Amount to reduce alpha from main text color for subtext.
  static const double _subtextAlphaReduction = 0.3;

  final String text;
  final String subtext;
  final void Function(String) onKeyPressed;

  @override
  State<KeypadKeyButton> createState() => _KeypadKeyButtonState();
}

class _KeypadKeyButtonState extends State<KeypadKeyButton> {
  DateTime? _pointerDownAt;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    final textStyle = theme.textTheme.headlineLarge?.copyWith(height: 1.0);

    // Derive subtext color from text color with reduced opacity if not set.
    Color? derivedSubColor = textStyle?.color;
    if (derivedSubColor != null) {
      var a = derivedSubColor.a - KeypadKeyButton._subtextAlphaReduction;
      if (a < KeypadKeyButton._minAlphaValue) a = KeypadKeyButton._minAlphaValue;
      derivedSubColor = derivedSubColor.withValues(alpha: a);
    }

    final subStyle = theme.textTheme.bodyMedium?.copyWith(
      color: derivedSubColor,
      height: 1.0,
    );

    final hasLongPress = widget.subtext.length == 1;

    // The pointer input stays on the Listener below; this node carries the
    // accessibility contract for the key. The subtree is excluded so the
    // decorative TextButton's no-op handler and the raw glyph texts do not
    // form nodes of their own - assistive-technology activation must reach
    // the same input path as a finger.
    return Semantics(
      identifier: 'keypad_key_${widget.text}',
      label: widget.subtext.isEmpty ? widget.text : '${widget.text} ${widget.subtext}',
      button: true,
      excludeSemantics: true,
      onTap: () => widget.onKeyPressed(widget.text),
      onLongPress: hasLongPress ? () => widget.onKeyPressed(widget.subtext) : null,
      child: Listener(
        key: Key(widget.text),
        onPointerDown: (_) {
          _pointerDownAt = DateTime.now();
          if (!hasLongPress) widget.onKeyPressed(widget.text);
        },
        onPointerUp: hasLongPress
            ? (_) {
                final downAt = _pointerDownAt;
                if (downAt == null) return;
                if (DateTime.now().difference(downAt) < kLongPressTimeout) {
                  widget.onKeyPressed(widget.text);
                }
              }
            : null,
        child: TextButton(
          onPressed: () {},
          onLongPress: hasLongPress ? () => widget.onKeyPressed(widget.subtext) : null,
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text(widget.text, style: textStyle),
              Padding(
                padding: KeypadKeyButton._subextPadding,
                child: Text(widget.subtext, style: subStyle),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
