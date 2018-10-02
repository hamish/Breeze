# Breeze

Breeze is a system for building cloudformation templates, and maintaining cloudformation stacks.



    usage: breeze command [options] 

    verge generate -v version_label output_directory -d breeze_project_directory
    breeze launch stack_name -p project_name -l version_label [-o parameter_name=value [-o parameter_name=value]
    breeze update_version stack_name -l version_label
    breeze launch_child_stack parent_stack_name -t template_name
    breeze delete_child_stack parent_stack_name -t template_name
    breeze apply_policy stack_name policy_name
    breeze remove_policy stack_name




