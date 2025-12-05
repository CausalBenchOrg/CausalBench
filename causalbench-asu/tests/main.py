from causalbench.modules import Dataset, Metric, Model, Context, Run, Task

def main():
    pass

    # task: Task = Task(module_id=1, version=1)
    # # print(task.name)
    # task.publish(public=True)

    # dataset: Dataset = Dataset(zip_file="C:\\Users\\prata\\Files\\Git\\CausalBench\\causalbench-asu\\tests\\data\\abalone.zip")
    # dataset.publish()

    # dataset: Dataset = Dataset(module_id=1, version=1)
    # # # print(dataset.name)
    # dataset.publish(public=True)

    task: Task = Task(zip_file="C:\\Users\\prata\\Files\\Git\\CausalBench\\causalbench-asu\\tests\\task\\discovery.static.zip")
    task.publish()

    # model: Model = Model(zip_file="C:\\Users\\prata\\Files\\Git\\CausalBench\\causalbench-asu\\tests\\model\\pc.zip")
    # model.publish()

    # model: Model = Model(module_id=1, version=1)
    # # # print(model.name)
    # model.publish(public=True)

    # metric: Metric = Metric(zip_file="C:\\Users\\prata\\Files\\Git\\CausalBench\\causalbench-asu\\tests\\metric\\accuracy_static.zip")
    # metric.publish()

    # metric: Metric = Metric(module_id=1, version=1)
    # # print(metric.name)
    # metric.publish(public=True)

    # context: Context = Context.create(
    #     name='Context1',
    #     description='Test static context',
    #     task=task,
    #     datasets=[(dataset, {'data': 'file1', 'ground_truth': 'file2'})],
    #     models=[(model, {})],
    #     metrics=[(metric, {})])
    
    # context.publish()
    
    # # run: Run = context.execute()
    # # print(run)


if __name__ == '__main__':
    main()
