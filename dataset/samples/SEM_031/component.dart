import 'package:flutter/material.dart';

enum TextFieldTypes { PLAIN_TEXT, PASSWORD }

class SmoothTextFormField extends StatefulWidget {
  const SmoothTextFormField({
    required this.type,
    required this.controller,
    required this.hintText,
    super.key,
    this.enabled,
    this.textInputAction,
    this.validator,
    this.autofillHints,
    this.onFieldSubmitted,
  });

  final TextFieldTypes type;
  final TextEditingController? controller;
  final String hintText;
  final bool? enabled;
  final TextInputAction? textInputAction;
  final String? Function(String?)? validator;
  final Iterable<String>? autofillHints;
  final ValueChanged<String>? onFieldSubmitted;

  @override
  State<SmoothTextFormField> createState() => _SmoothTextFormFieldState();
}

class _SmoothTextFormFieldState extends State<SmoothTextFormField> {
  late bool _obscureText;

  @override
  void initState() {
    _obscureText = widget.type == TextFieldTypes.PASSWORD;
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    final bool enableSuggestions = widget.type == TextFieldTypes.PLAIN_TEXT;
    final bool autocorrect = widget.type == TextFieldTypes.PLAIN_TEXT;

    return TextFormField(
      controller: widget.controller,
      enabled: widget.enabled,
      textInputAction: widget.textInputAction,
      validator: widget.validator,
      obscureText: _obscureText,
      enableSuggestions: enableSuggestions,
      autocorrect: autocorrect,
      autofillHints: widget.autofillHints,
      autovalidateMode: AutovalidateMode.onUserInteraction,
      onFieldSubmitted: widget.onFieldSubmitted,
      decoration: InputDecoration(
        contentPadding: const EdgeInsets.symmetric(
          horizontal: 16.0,
          vertical: 8.0,
        ),
        filled: true,
        hintText: widget.hintText,
        hintMaxLines: 2,
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(30.0),
          borderSide: const BorderSide(color: Colors.transparent, width: 5.0),
        ),
        suffixIcon: widget.type == TextFieldTypes.PASSWORD
            ? IconButton(
                tooltip: 'Show Password',
                splashRadius: 10.0,
                onPressed: () => setState(() {
                  _obscureText = !_obscureText;
                }),
                icon: _obscureText
                    ? const Icon(Icons.visibility_off, size: 18.0)
                    : const Icon(Icons.visibility, size: 18.0),
              )
            : null,
        errorMaxLines: 2,
      ),
    );
  }
}
