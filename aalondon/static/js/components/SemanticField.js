import React from 'react';
import { Field } from 'formik';
import { Radio,Checkbox } from 'semantic-ui-react';

const SemanticField = ({ component, ...fieldProps }) => {
  const { showErrorsInline, ...rest } = fieldProps;

  return (
    <Field {...rest}>
      {({
        field: { value, onBlur, ...field },
        form: { setFieldValue, submitCount, touched, errors, handleBlur },
        ...props
      }) => {
        return React.createElement(component, {
          ...rest,
          ...field,
          ...props,
          ...(component === Radio || component === Checkbox
            ? {
                checked:
                  component === Radio ? fieldProps.value === value : value,
              }
            : {
                value: value || '',
              }),

          ...((submitCount >= 1 || touched[field.name]) && errors[field.name]
            ? {
                error:
                  showErrorsInline == false
                    ? true
                    : {
                        content: errors[field.name],
                      },
              }
            : {}),
          onChange: (e, { value: newValue, checked }) =>
            setFieldValue(fieldProps.name, newValue || checked),
          onBlur: handleBlur,
        });
      }}
    </Field>
  );
};

export default SemanticField;
