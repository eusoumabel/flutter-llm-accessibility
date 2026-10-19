import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

class ShareUrlRow extends StatelessWidget {
  const ShareUrlRow({
    required this.url,
    required this.onShowQrCode,
    required this.onShowZoom,
    super.key,
  });

  final String url;
  final VoidCallback onShowQrCode;
  final VoidCallback onShowZoom;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(5),
      child: Row(
        children: [
          SelectableText(
            url,
            style: Theme.of(context).textTheme.bodyMedium,
          ),
          const SizedBox(width: 5),
          InkWell(
            onTap: () async {
              await Clipboard.setData(ClipboardData(text: url));
              if (context.mounted) {
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text('Copied to Clipboard')),
                );
              }
            },
            child: const Padding(
              padding: EdgeInsets.symmetric(horizontal: 8, vertical: 2),
              child: Icon(Icons.content_copy, size: 16),
            ),
          ),
          InkWell(
            onTap: onShowQrCode,
            child: const Padding(
              padding: EdgeInsets.symmetric(horizontal: 8, vertical: 2),
              child: Icon(Icons.qr_code, size: 16),
            ),
          ),
          InkWell(
            onTap: onShowZoom,
            child: const Padding(
              padding: EdgeInsets.symmetric(horizontal: 8, vertical: 2),
              child: Icon(Icons.tv, size: 16),
            ),
          ),
        ],
      ),
    );
  }
}
