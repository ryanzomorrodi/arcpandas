# -*- coding: utf-8 -*-

import arcpy
import helpers

import numpy as np

import importlib
importlib.reload(helpers)

class Toolbox:
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "arcpandas"
        self.alias = "arcpandas"

        # List of tool classes associated with this toolbox
        self.tools = [Join]

class Join:
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Join"
        self.description = ""

    def getParameterInfo(self):
        """Define the tool parameters."""
        param_input_table = arcpy.Parameter(
            displayName="Input Table",
            name="InputTable",
            datatype="GPTableView",
            parameterType="Required",
            direction="Input"
        )

        param_input_table_fields = arcpy.Parameter(
            displayName="Input Table Fields",
            name="InputTableFields",
            datatype="GPValueTable",
            parameterType="Required",
            direction="Input"
        )
        param_input_table_fields.parameterDependencies = [param_input_table.name]
        param_input_table_fields.columns = [['Field', 'Field']]

        param_join_table = arcpy.Parameter(
            displayName="Join Table",
            name="JoinTable",
            datatype="GPTableView",
            parameterType="Required",
            direction="Input"
        )

        param_join_table_fields = arcpy.Parameter(
            displayName="Join Table Fields",
            name="JoinTableFields",
            datatype="GPValueTable",
            parameterType="Required",
            direction="Input"
        )
        param_join_table_fields.parameterDependencies = [param_join_table.name]
        param_join_table_fields.columns = [['Field', 'Field']]

        param_join_type = arcpy.Parameter(
            displayName="Type",
            name="JoinType",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        param_join_type.filter.list = ["left", "right", "outer", "inner", "anti"]

        param_output_table = arcpy.Parameter(
            displayName="Output Table",
            name="OutputTable",
            datatype="GPTableView",
            parameterType="Required",
            direction="Output"
        )

        params = [
            param_input_table,
            param_input_table_fields,
            param_join_table,
            param_join_table_fields,
            param_join_type,
            param_output_table
        ]

        return params

    def isLicensed(self):
        """Set whether the tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter. This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""

        param_input_table = parameters[0]
        param_input_table_fields = parameters[1]
        param_join_table = parameters[2]
        param_join_table_fields = parameters[3]
        param_join_type = parameters[4]
        param_output_table = parameters[5]

        input_table = helpers.get_pandas(param_input_table)
        input_table_join_fields = helpers.get_value_table_fields(param_input_table_fields)

        join_table = helpers.get_pandas(param_join_table)
        join_table_join_fields = helpers.get_value_table_fields(param_join_table_fields)

        if (param_join_type.valueAsText == "anti"):
            output = input_table.merge(
                join_table, 
                how = "outer",
                left_on = input_table_join_fields, 
                right_on = join_table_join_fields,
                indicator = True
            ).query('_merge == "left_only"')

            join_table_fields = helpers.get_table_fields(param_join_table)

            output = output.drop(join_table_fields + ["_merge"], axis = 1, errors = "ignore")
        else:
            output = input_table.merge(
                join_table, 
                how = param_join_type.valueAsText,
                left_on = input_table_join_fields, 
                right_on = join_table_join_fields
            )
            
        helpers.write_table(output, param_output_table)

        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return
