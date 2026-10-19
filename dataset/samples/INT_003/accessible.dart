import 'package:flutter/material.dart';

class AttachmentThumbnail extends StatelessWidget {
  final String fileName;
  final VoidCallback onRemove;

  const AttachmentThumbnail({
    super.key,
    required this.fileName,
    required this.onRemove,
  });

  @override
  Widget build(BuildContext context) {
    return Stack(
      children: [
        Container(
          width: 120,
          height: 120,
          alignment: Alignment.center,
          padding: const EdgeInsets.all(8),
          decoration: BoxDecoration(
            color: Colors.grey.shade300,
            borderRadius: BorderRadius.circular(8),
          ),
          child: Text(fileName, overflow: TextOverflow.ellipsis),
        ),
        Positioned(
          top: 0,
          right: 0,
          child: Semantics(
            button: true,
            label: 'Remove $fileName',
            child: InkWell(
              onTap: onRemove,
              customBorder: const CircleBorder(),
              child: const SizedBox(
                width: 48,
                height: 48,
                child: Center(
                  child: CircleAvatar(
                    radius: 10,
                    child: Icon(Icons.close, size: 14),
                  ),
                ),
              ),
            ),
          ),
        ),
      ],
    );
  }
}
