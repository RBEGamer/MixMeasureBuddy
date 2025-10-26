const basePath = process.env.NEXT_PUBLIC_BASE_PATH ?? '';

const isAbsoluteUrl = (value: string) => /^([a-z]+:)?\/\//i.test(value);

export const withBasePath = (value: string): string => {
  if (!value) {
    return value;
  }

  if (isAbsoluteUrl(value)) {
    return value;
  }

  if (basePath && value.startsWith('/')) {
    return `${basePath}${value}`;
  }

  if (basePath && !value.startsWith('/')) {
    return `${basePath}/${value}`;
  }

  return value;
};

export { basePath };
