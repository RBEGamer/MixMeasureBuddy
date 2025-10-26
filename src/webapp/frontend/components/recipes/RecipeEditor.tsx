'use client';

import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { useFieldArray, useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import {
  recipeSchema,
  type Recipe,
  type RecipeStep,
  createEmptyRecipe,
  slugifyRecipeName,
  parseRecipeJson,
  stringifyRecipe,
  RecipeAction,
  type RecipeActionValue,
} from '@/lib/recipes';
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/shared/ui/card';
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/shared/ui/form';
import { Input } from '@/components/shared/ui/input';
import { Textarea } from '@/components/shared/ui/textarea';
import { Button } from '@/components/shared/ui/button';
import { Badge } from '@/components/shared/ui/badge';
import { ScrollArea } from '@/components/shared/ui/scroll-area';
import { Separator } from '@/components/shared/ui/separator';
import {
  ArrowDown,
  ArrowUp,
  BookOpen,
  Download,
  FilePlus2,
  Loader2,
  RefreshCw,
  Trash2,
  Upload,
  Search,
} from 'lucide-react';
import { toast } from 'sonner';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuTrigger,
} from '@/components/shared/ui/dropdown-menu';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/shared/ui/select';

type SampleRecipe = Recipe & { filename: string };

const SAMPLE_DATA_ENDPOINT = '/data/sample-recipes.json';

type StepTypeDefinition = {
  id: RecipeActionValue;
  dropdownLabel: string;
  description: string;
  ingredientLabel: string;
  ingredientDisabled: boolean;
  defaultIngredient?: string;
  amountLabel: string;
  amountHelper?: string;
  amountPlaceholder?: string;
  amountDisabled: boolean;
  defaultAmount: number;
  textPlaceholder: string;
  defaultText?: string;
};

const STEP_TYPE_DEFINITIONS: Record<RecipeActionValue, StepTypeDefinition> = {
  [RecipeAction.SCALE]: {
    id: RecipeAction.SCALE,
    dropdownLabel: 'Scale — weigh until the target mass is reached',
    description: 'Prompts the user to pour until the scale reaches the desired weight.',
    ingredientLabel: 'Ingredient',
    ingredientDisabled: false,
    amountLabel: 'Target weight (grams)',
    amountHelper: 'Use grams. MixMeasureBuddy stops pouring once this value is reached.',
    amountPlaceholder: 'e.g. 45',
    amountDisabled: false,
    defaultAmount: 30,
    textPlaceholder: 'Describe what to do while weighing.',
  },
  [RecipeAction.WAIT]: {
    id: RecipeAction.WAIT,
    dropdownLabel: 'Wait — pause for a number of seconds',
    description: 'Shows a countdown so the mixture can infuse or settle before continuing.',
    ingredientLabel: 'Ingredient',
    ingredientDisabled: true,
    amountLabel: 'Wait time (seconds)',
    amountHelper: 'How long MixMeasureBuddy should wait before the next step.',
    amountPlaceholder: 'e.g. 15',
    amountDisabled: false,
    defaultAmount: 10,
    textPlaceholder: 'Describe what happens during the wait.',
    defaultText: 'Let the mixture rest.',
  },
  [RecipeAction.CONFIRM]: {
    id: RecipeAction.CONFIRM,
    dropdownLabel: 'Confirm — ask the user to continue',
    description: 'Useful for manual actions such as stirring or garnishing.',
    ingredientLabel: 'Ingredient (optional)',
    ingredientDisabled: false,
    amountLabel: 'No numeric target required',
    amountHelper: 'Confirm steps do not use a numeric amount.',
    amountPlaceholder: '',
    amountDisabled: true,
    defaultAmount: -1,
    textPlaceholder: 'Describe what to confirm before continuing.',
    defaultText: 'Confirm to continue.',
  },
};

const STEP_TYPE_ORDER: RecipeActionValue[] = [
  RecipeAction.SCALE,
  RecipeAction.WAIT,
  RecipeAction.CONFIRM,
];

const cloneRecipe = (recipe: Recipe): Recipe =>
  JSON.parse(JSON.stringify(recipe)) as Recipe;

const downloadAsRecipeFile = (recipe: Recipe) => {
  const filename = recipe.filename?.trim().length
    ? recipe.filename.trim()
    : slugifyRecipeName(recipe.name || 'recipe');
  const blob = new Blob([stringifyRecipe(recipe)], {
    type: 'application/json',
  });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
};

export function RecipeEditor(): JSX.Element {
  const [availableSamples, setAvailableSamples] = useState<SampleRecipe[]>([]);
  const [loadingSamples, setLoadingSamples] = useState<boolean>(false);
  const [samplesLoaded, setSamplesLoaded] = useState<boolean>(false);
  const [samplesError, setSamplesError] = useState<string | null>(null);
  const [sampleQuery, setSampleQuery] = useState<string>('');
  const [isNewRecipe, setIsNewRecipe] = useState<boolean>(true);
  const [filenameManuallyEdited, setFilenameManuallyEdited] =
    useState<boolean>(false);
  const [lastSourceLabel, setLastSourceLabel] =
    useState<string>('Blank recipe');
  const [exporting, setExporting] = useState<boolean>(false);

  const baselineRecipeRef = useRef<Recipe>(createEmptyRecipe());
  const uploadInputRef = useRef<HTMLInputElement | null>(null);

  const form = useForm<Recipe>({
    resolver: zodResolver(recipeSchema),
    defaultValues: createEmptyRecipe(),
    mode: 'onChange',
  });

  const {
    control,
    handleSubmit,
    reset,
    setValue,
    getValues,
    watch,
    formState: { isDirty, isSubmitting },
  } = form;

  const {
    fields: stepFields,
    append: appendStep,
    remove: removeStep,
    move: moveStep,
  } = useFieldArray({
    control,
    name: 'steps',
  });

  const steps = watch('steps');

  const recipeName = watch('name');

  useEffect(() => {
    if (!isNewRecipe || filenameManuallyEdited) {
      return;
    }

    const source = recipeName?.trim().length ? recipeName : 'New Recipe';
    setValue('filename', slugifyRecipeName(source), {
      shouldDirty: true,
    });
  }, [recipeName, isNewRecipe, filenameManuallyEdited, setValue]);

  useEffect(() => {
    let cancelled = false;

    const loadSamples = async () => {
      setLoadingSamples(true);
      setSamplesError(null);
      try {
        const response = await fetch(SAMPLE_DATA_ENDPOINT, {
          cache: 'force-cache',
        });
        if (!response.ok) {
          throw new Error(`Server responded with ${response.status}`);
        }

        const payload = (await response.json()) as unknown;
        const parsedResult = recipeSchema.array().safeParse(payload);
        const parsed = parsedResult.success
          ? (parsedResult.data as SampleRecipe[])
          : [];

        if (!cancelled) {
          setAvailableSamples(parsed);
          setSamplesLoaded(true);
          if (!parsed.length) {
            setSamplesError('No sample recipes were found.');
          }
        }
      } catch (error) {
        if (!cancelled) {
          console.warn('[RecipeEditor] Failed to load sample recipes:', error);
          setSamplesError('Unable to load sample recipes right now.');
        }
      } finally {
        if (!cancelled) {
          setLoadingSamples(false);
        }
      }
    };

    loadSamples();

    return () => {
      cancelled = true;
    };
  }, []);

  const filteredSamples = useMemo(() => {
    if (!sampleQuery.trim().length) {
      return availableSamples;
    }
    const query = sampleQuery.toLowerCase();
    return availableSamples.filter(
      (recipe) =>
        recipe.name.toLowerCase().includes(query) ||
        recipe.filename.toLowerCase().includes(query) ||
        recipe.description.toLowerCase().includes(query),
    );
  }, [availableSamples, sampleQuery]);

  const loadRecipeIntoForm = useCallback(
    (recipe: Recipe, sourceLabel: string, markAsNew: boolean) => {
      const snapshot = cloneRecipe(recipe);
      baselineRecipeRef.current = snapshot;
      reset(snapshot);
      setIsNewRecipe(markAsNew);
      setFilenameManuallyEdited(!markAsNew);
      setLastSourceLabel(sourceLabel);
      toast.success(`Loaded ${recipe.name}`);
    },
    [reset],
  );

  const handleStartBlank = () => {
    const blank = createEmptyRecipe();
    loadRecipeIntoForm(blank, 'Blank recipe', true);
  };

  const handleSampleSelect = (recipe: Recipe) => {
    loadRecipeIntoForm(recipe, `Sample: ${recipe.name}`, false);
  };

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) {
      return;
    }

    try {
      const text = await file.text();
      const parsed = parseRecipeJson(text);
      loadRecipeIntoForm(parsed, `Uploaded: ${file.name}`, false);
    } catch (error) {
      console.error('[RecipeEditor] Failed to parse uploaded recipe:', error);
      toast.error('Could not read that file. Ensure it is a valid .recipe JSON.');
    } finally {
      event.target.value = '';
    }
  };

  const handleResetChanges = () => {
    const baseline = baselineRecipeRef.current;
    reset(cloneRecipe(baseline));
    setFilenameManuallyEdited(!isNewRecipe);
    toast.info('Reverted to the last loaded recipe.');
  };

  const handleDownloadRecipe = handleSubmit(async (values) => {
    setExporting(true);
    try {
      downloadAsRecipeFile(values);
      toast.success(`Downloaded ${values.filename}`);
    } catch (error) {
      console.error('[RecipeEditor] Failed to download recipe:', error);
      toast.error('Something went wrong while generating the download.');
    } finally {
      setExporting(false);
    }
  });

  const applyActionSideEffects = useCallback(
    (index: number, action: RecipeActionValue) => {
      const definition = STEP_TYPE_DEFINITIONS[action];

      if (definition.ingredientDisabled) {
        setValue(`steps.${index}.ingredient`, definition.defaultIngredient ?? '', {
          shouldDirty: true,
        });
      }

      const latestSteps = getValues('steps');
      const currentAmount = latestSteps?.[index]?.amount;
      if (definition.amountDisabled) {
        setValue(`steps.${index}.amount`, definition.defaultAmount, {
          shouldDirty: true,
        });
      } else if (
        typeof currentAmount !== 'number' ||
        Number.isNaN(currentAmount) ||
        currentAmount < 0
      ) {
        setValue(`steps.${index}.amount`, definition.defaultAmount, {
          shouldDirty: true,
        });
      }

      const currentText = latestSteps?.[index]?.text ?? '';
      if (!currentText.trim() && definition.defaultText) {
        setValue(`steps.${index}.text`, definition.defaultText, {
          shouldDirty: true,
        });
      }
    },
    [getValues, setValue],
  );

  const createStepForActionType = (action: RecipeActionValue): RecipeStep => {
    const definition = STEP_TYPE_DEFINITIONS[action];
    const ingredientBase = definition.defaultIngredient ?? '';
    return {
      action,
      amount: definition.defaultAmount,
      ingredient: ingredientBase,
      text: definition.defaultText ?? '',
    };
  };

  const handleAddStep = (action: RecipeActionValue) => {
    appendStep(createStepForActionType(action));
  };

  const handleMoveStep = (from: number, to: number) => {
    if (to < 0 || to >= stepFields.length) {
      return;
    }
    moveStep(from, to);
  };

  return (
    <div className="flex w-full flex-col gap-8">
      <div className="grid w-full gap-6 lg:grid-cols-[minmax(280px,320px)_1fr]">
        <div className="flex flex-col gap-6">
          <Card className="h-fit">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-xl">
                <BookOpen className="h-5 w-5" />
                Recipe sources
              </CardTitle>
              <CardDescription>
                Start from scratch, upload your own file, or explore the bundled
                cocktail library.
              </CardDescription>
            </CardHeader>
            <CardContent className="flex flex-col gap-3">
              <Button variant="outlinePrimary" onClick={handleStartBlank}>
                <FilePlus2 className="mr-2 h-4 w-4" />
                Start a blank recipe
              </Button>
              <input
                ref={uploadInputRef}
                type="file"
                accept=".recipe,application/json"
                className="hidden"
                onChange={handleFileUpload}
              />
              <Button
                variant="outline"
                onClick={() => uploadInputRef.current?.click()}
              >
                <Upload className="mr-2 h-4 w-4" />
                Upload an existing .recipe file
              </Button>
            </CardContent>
            <CardFooter className="flex flex-col gap-2">
              <Badge variant="outline" className="text-xs font-medium w-fit">
                Loaded from: {lastSourceLabel}
              </Badge>
              <p className="text-xs text-muted-foreground">
                Your edits stay in the browser until you download the file.
              </p>
            </CardFooter>
          </Card>

          <Card className="flex h-[420px] flex-col">
            <CardHeader>
              <CardTitle className="text-lg">Sample recipe library</CardTitle>
              <CardDescription>
                Browse the built-in collection shipped with MixMeasureBuddy.
              </CardDescription>
            </CardHeader>
            <CardContent className="flex flex-col gap-4">
              <div className="relative">
                <Input
                  placeholder="Search sample recipes..."
                  value={sampleQuery}
                  onChange={(event) => setSampleQuery(event.target.value)}
                  className="pl-9"
                />
                <Search className="absolute left-2 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
              </div>
              <Separator />
              <ScrollArea className="h-[260px]">
                <div className="flex flex-col gap-2 pr-2">
                  {loadingSamples && (
                    <div className="flex items-center gap-2 rounded-md border border-dashed p-3 text-sm text-muted-foreground">
                      <Loader2 className="h-4 w-4 animate-spin" />
                      Fetching sample library…
                    </div>
                  )}
                  {!loadingSamples && samplesError && (
                    <div className="rounded-md border border-destructive/40 bg-destructive/10 p-3 text-sm text-destructive">
                      {samplesError}
                    </div>
                  )}
                  {!loadingSamples &&
                    !samplesError &&
                    filteredSamples.length === 0 &&
                    samplesLoaded && (
                      <div className="rounded-md border border-dashed p-3 text-sm text-muted-foreground">
                        No samples match “{sampleQuery}”.
                      </div>
                    )}
                  {filteredSamples.map((recipe) => (
                    <Button
                      key={recipe.filename}
                      variant="outline"
                      size="sm"
                      className="justify-start text-left"
                      onClick={() => handleSampleSelect(recipe)}
                    >
                      <span className="truncate">
                        {recipe.name}{' '}
                        <span className="text-xs text-muted-foreground">
                          ({recipe.filename})
                        </span>
                      </span>
                    </Button>
                  ))}
                </div>
              </ScrollArea>
            </CardContent>
          </Card>
        </div>

        <Card className="flex flex-col">
          <Form {...form}>
            <form
              className="flex h-full flex-col"
              onSubmit={handleDownloadRecipe}
              noValidate
            >
              <CardHeader className="space-y-4">
                <div className="flex flex-col gap-2">
                  <CardTitle className="text-2xl">
                    {isNewRecipe ? 'Create a recipe' : 'Edit recipe'}
                  </CardTitle>
                  <CardDescription>
                    Structure each step, adjust amounts, and download the finished
                    <code className="ml-1 text-xs">.recipe</code> file for your scale.
                  </CardDescription>
                </div>
                <div className="grid gap-4 md:grid-cols-2">
                  <FormField
                    control={control}
                    name="name"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Recipe name</FormLabel>
                        <FormControl>
                          <Input placeholder="Old Fashioned" {...field} />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                  <FormField
                    control={control}
                    name="filename"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Filename</FormLabel>
                        <FormControl>
                          <Input
                            placeholder="old_fashioned.recipe"
                            {...field}
                            onChange={(event) => {
                              if (!filenameManuallyEdited) {
                                setFilenameManuallyEdited(true);
                              }
                              field.onChange(event.target.value);
                            }}
                          />
                        </FormControl>
                        <FormDescription>
                          Exported as <code>{field.value || '<filename>'}</code>
                        </FormDescription>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                </div>
                <FormField
                  control={control}
                  name="description"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Description</FormLabel>
                      <FormControl>
                        <Textarea
                          rows={3}
                          placeholder="Describe what makes this recipe special."
                          {...field}
                        />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </CardHeader>

              <CardContent className="flex-1 space-y-6 overflow-auto">
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <h3 className="text-lg font-semibold">Steps</h3>
                    <DropdownMenu>
                      <DropdownMenuTrigger asChild>
                        <Button type="button" size="sm" variant="outlinePrimary">
                          Add step
                        </Button>
                      </DropdownMenuTrigger>
                      <DropdownMenuContent align="end" className="w-72">
                        <DropdownMenuLabel>Select step type</DropdownMenuLabel>
                        {STEP_TYPE_ORDER.map((action) => {
                          const definition = STEP_TYPE_DEFINITIONS[action];
                          return (
                            <DropdownMenuItem
                              key={action}
                              className="flex flex-col items-start gap-1 whitespace-normal"
                              onClick={() => handleAddStep(action)}
                            >
                              <span className="font-medium">
                                {definition.dropdownLabel.split(' — ')[0]}
                              </span>
                              <span className="text-xs text-muted-foreground">
                                {definition.description}
                              </span>
                            </DropdownMenuItem>
                          );
                        })}
                      </DropdownMenuContent>
                    </DropdownMenu>
                  </div>
                  <div className="flex flex-col gap-4">
                    {stepFields.map((field, index) => {
                      const currentAction = Number(
                        steps?.[index]?.action ?? RecipeAction.SCALE,
                      ) as RecipeActionValue;
                      const actionDefinition =
                        STEP_TYPE_DEFINITIONS[currentAction] ??
                        STEP_TYPE_DEFINITIONS[RecipeAction.SCALE];

                      return (
                        <div
                          key={field.id}
                          className="rounded-lg border border-dashed p-4 shadow-sm"
                        >
                        <div className="mb-3 flex items-center justify-between">
                          <div className="flex items-center gap-2">
                            <Badge variant="outline">Step {index + 1}</Badge>
                          </div>
                          <div className="flex items-center gap-1">
                            <Button
                              type="button"
                              variant="ghost"
                              size="icon"
                              onClick={() => handleMoveStep(index, index - 1)}
                              disabled={index === 0}
                              aria-label="Move step up"
                            >
                              <ArrowUp className="h-4 w-4" />
                            </Button>
                            <Button
                              type="button"
                              variant="ghost"
                              size="icon"
                              onClick={() => handleMoveStep(index, index + 1)}
                              disabled={index === stepFields.length - 1}
                              aria-label="Move step down"
                            >
                              <ArrowDown className="h-4 w-4" />
                            </Button>
                            <Button
                              type="button"
                              variant="ghost"
                              size="icon"
                              onClick={() => removeStep(index)}
                              disabled={stepFields.length === 1}
                              aria-label="Remove step"
                            >
                              <Trash2 className="h-4 w-4" />
                            </Button>
                          </div>
                        </div>

                        <div className="grid gap-3 md:grid-cols-2">
                          <FormField
                            control={control}
                            name={`steps.${index}.action`}
                            render={({ field: stepField }) => (
                              <FormItem>
                                <FormLabel>Step type</FormLabel>
                                <Select
                                  value={String(stepField.value ?? currentAction)}
                                  onValueChange={(value) => {
                                    const numericAction = Number(value) as RecipeActionValue;
                                    stepField.onChange(numericAction);
                                    applyActionSideEffects(index, numericAction);
                                  }}
                                >
                                  <FormControl>
                                    <SelectTrigger>
                                      <SelectValue />
                                    </SelectTrigger>
                                  </FormControl>
                                  <SelectContent>
                                    {STEP_TYPE_ORDER.map((action) => (
                                      <SelectItem
                                        key={action}
                                        value={String(action)}
                                      >
                                        {
                                          STEP_TYPE_DEFINITIONS[action]
                                            .dropdownLabel
                                        }
                                      </SelectItem>
                                    ))}
                                  </SelectContent>
                                </Select>
                                <FormDescription>
                                  {actionDefinition.description}
                                </FormDescription>
                                <FormMessage />
                              </FormItem>
                            )}
                          />
                          <FormField
                            control={control}
                            name={`steps.${index}.ingredient`}
                            render={({ field: stepField }) => (
                              <FormItem>
                                <FormLabel>
                                  {actionDefinition.ingredientLabel}
                                </FormLabel>
                                <FormControl>
                                  <Input
                                    placeholder="Bourbon Whiskey"
                                    disabled={actionDefinition.ingredientDisabled}
                                    {...stepField}
                                  />
                                </FormControl>
                                <FormMessage />
                              </FormItem>
                            )}
                          />
                          <FormField
                            control={control}
                            name={`steps.${index}.amount`}
                            render={({ field: stepField }) => (
                              <FormItem>
                                <FormLabel>{actionDefinition.amountLabel}</FormLabel>
                                <FormControl>
                                  <Input
                                    type="number"
                                    inputMode="decimal"
                                    value={
                                      Number.isFinite(stepField.value as number)
                                        ? (stepField.value as number)
                                        : ''
                                    }
                                    onChange={(event) =>
                                      stepField.onChange(
                                        event.target.value === ''
                                          ? Number.NaN
                                          : event.target.valueAsNumber,
                                      )
                                    }
                                    disabled={actionDefinition.amountDisabled}
                                    placeholder={actionDefinition.amountPlaceholder}
                                  />
                                </FormControl>
                                {actionDefinition.amountHelper ? (
                                  <FormDescription>
                                    {actionDefinition.amountHelper}
                                  </FormDescription>
                                ) : null}
                                <FormMessage />
                              </FormItem>
                            )}
                          />
                        </div>

                        <div className="grid gap-3 md:grid-cols-2">
                          <FormField
                            control={control}
                            name={`steps.${index}.action`}
                            render={({ field: stepField }) => (
                              <FormItem>
                                <FormLabel>Action code</FormLabel>
                                <FormControl>
                                  <Input
                                    type="number"
                                    inputMode="numeric"
                                    value={
                                      Number.isFinite(stepField.value as number)
                                        ? (stepField.value as number)
                                        : ''
                                    }
                                    onChange={(event) =>
                                      stepField.onChange(
                                        event.target.value === ''
                                          ? Number.NaN
                                          : event.target.valueAsNumber,
                                      )
                                    }
                                  />
                                </FormControl>
                                <FormDescription>
                                  Matches the firmware&apos;s action identifiers.
                                </FormDescription>
                                <FormMessage />
                              </FormItem>
                            )}
                          />
                          <FormField
                            control={control}
                            name={`steps.${index}.text`}
                            render={({ field: stepField }) => (
                              <FormItem>
                                <FormLabel>Instruction</FormLabel>
                                <FormControl>
                                  <Textarea
                                    rows={2}
                                    placeholder={actionDefinition.textPlaceholder}
                                    {...stepField}
                                  />
                                </FormControl>
                                <FormMessage />
                              </FormItem>
                            )}
                          />
                        </div>
                      </div>
                    );
                    })}
                  </div>
                </div>
              </CardContent>

              <CardFooter className="flex flex-col gap-4 border-t bg-muted/30 p-6">
                <div className="flex flex-wrap items-center justify-between gap-3">
                  <Badge variant="outline" className="text-xs font-medium">
                    {isDirty ? 'Unsaved changes' : 'Up to date'}
                  </Badge>
                  <div className="flex flex-wrap gap-2">
                    <Button
                      type="button"
                      variant="outline"
                      onClick={handleResetChanges}
                      disabled={!isDirty}
                    >
                      <RefreshCw className="mr-2 h-4 w-4" />
                      Reset changes
                    </Button>
                    <Button
                      type="submit"
                      disabled={isSubmitting || exporting}
                    >
                      {isSubmitting || exporting ? (
                        <>
                          <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                          Preparing download…
                        </>
                      ) : (
                        <>
                          <Download className="mr-2 h-4 w-4" />
                          Download .recipe
                        </>
                      )}
                    </Button>
                  </div>
                </div>
              </CardFooter>
            </form>
          </Form>
        </Card>
      </div>
    </div>
  );
}
