import 'package:flutter/material.dart';

class TaskBoard extends StatefulWidget {
  final List<String> initialTasks;

  const TaskBoard({super.key, required this.initialTasks});

  @override
  State<TaskBoard> createState() => _TaskBoardState();
}

class _TaskBoardState extends State<TaskBoard> {
  late final List<String> _todo = List.of(widget.initialTasks);
  final List<String> _done = [];

  void _markDone(String task) {
    setState(() {
      _todo.remove(task);
      _done.add(task);
    });
  }

  @override
  Widget build(BuildContext context) {
    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Expanded(
          child: Column(
            children: [
              Semantics(header: true, child: const Text('To do')),
              for (final task in _todo)
                LongPressDraggable<String>(
                  data: task,
                  feedback: Material(
                    elevation: 4,
                    child: SizedBox(
                      width: 160,
                      child: ListTile(title: Text(task)),
                    ),
                  ),
                  child: Card(
                    child: ListTile(title: Text(task)),
                  ),
                ),
            ],
          ),
        ),
        Expanded(
          child: DragTarget<String>(
            onAcceptWithDetails: (details) => _markDone(details.data),
            builder: (context, candidates, rejected) => Column(
              children: [
                Semantics(header: true, child: const Text('Done')),
                for (final task in _done)
                  Card(child: ListTile(title: Text(task))),
              ],
            ),
          ),
        ),
      ],
    );
  }
}
