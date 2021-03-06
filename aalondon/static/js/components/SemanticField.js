import React from 'react';
import { Field } from 'formik';
import { Radio, Checkbox, Dropdown } from 'semantic-ui-react';

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
            : (component === Dropdown && fieldProps.multiple === true) ? {
              value: value || [],
              error: false
            } : {
                value: value || '',
              }),

          ...((submitCount >= 1 || touched[field.name]) && errors[field.name]
            ? {
              error:

                //showErrorsInline == false
                (component === Dropdown & fieldProps.multiple === true)
                  ? true
                  : {
                    content: errors[field.name],
                  },
            }
            : {}),
          onChange: (e, { value: newValue, checked }) =>{
            setFieldValue(fieldProps.name, newValue || checked)
           if (fieldProps.onChange){
              fieldProps.onChange(e,newValue,setFieldValue)
            }
          },
          onBlur: handleBlur,
        });
      }}
    </Field>
  );
};

export default SemanticField;


