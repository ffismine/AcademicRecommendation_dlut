package cf;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.FileSplit;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;
import java.util.regex.Pattern;


/**
 把主题词同现矩阵和使用次数得分矩阵相乘

 */
class MR4 {

	static void run(Configuration config, Map<String, String> paths) {
		try {
			FileSystem fs = FileSystem.get(config);
			Job job = Job.getInstance(config);
			job.setJobName("step4");
			job.setJarByClass(StartRun.class);
			job.setMapperClass(Step4_Mapper.class);
			job.setReducerClass(Step4_Reducer.class);
			job.setMapOutputKeyClass(Text.class);
			job.setMapOutputValueClass(Text.class);

			// FileInputFormat.addInputPath(job, new
			// Path(paths.get("Step4Input")));
			FileInputFormat.setInputPaths(job,
					new Path(paths.get("Step4Input1")),
					new Path(paths.get("Step4Input2")));
			Path outpath = new Path(paths.get("Step4Output"));
			if (fs.exists(outpath)) {
				fs.delete(outpath, true);
			}
			FileOutputFormat.setOutputPath(job, outpath);

			job.waitForCompletion(true);
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	static class Step4_Mapper extends Mapper<LongWritable, Text, Text, Text> {
		private String flag;// A同现矩阵 or B得分矩阵

		//每个maptask，初始化时调用一次
		protected void setup(Context context) throws IOException,
				InterruptedException {
			FileSplit split = (FileSplit) context.getInputSplit();
			flag = split.getPath().getParent().getName();// 判断读的数据集

			System.out.println(flag + "**********************");
		}

		protected void map(LongWritable key, Text value, Context context)
				throws IOException, InterruptedException {

			String[] tokens = Pattern.compile("[\t,]").split(value.toString());
			if (flag.equals("step3")) {// 同现矩阵
				//i100:i125	1
				String[] v1 = tokens[0].split(":");
				String itemID1 = v1[0];
				String itemID2 = v1[1];
				String num = tokens[1];
				//A:B 3
				//B:A 3
				Text k = new Text(itemID1);// 以前一个主题词为key 比如i100
				Text v = new Text("A:" + itemID2 + "," + num);// A:i109,1

				context.write(k, v);

			} else if (flag.equals("step2")) {// 学者对主题词得分矩阵
				
				//u26	i276:1,i201:1,i348:1,i321:1,i136:1,
				String userID = tokens[0];
				for (int i = 1; i < tokens.length; i++) {
					String[] vector = tokens[i].split(":");
					String itemID = vector[0];// itemid
					String pref = vector[1];// score

					Text k = new Text(itemID); // 以item为key 比如：i100
					Text v = new Text("B:" + userID + "," + pref); // B:u401,2

					context.write(k, v);
				}
			}
		}
	}

	static class Step4_Reducer extends Reducer<Text, Text, Text, Text> {
		protected void reduce(Text key, Iterable<Text> values, Context context)
				throws IOException, InterruptedException {
			// A同现矩阵 or B得分矩阵
			Map<String, Integer> mapA = new HashMap<String, Integer>();// 和该item（key中的itemID）同现的其他item的同现集合// 。其他物品ID为map的key，同现数字为值
			Map<String, Integer> mapB = new HashMap<String, Integer>();// 该item（key中的itemID），所有user的推荐权重分数。

			
			//A  > reduce   相同的KEY为一组
			//value:2类:
			//同现A:b:2  c:4   d:8
			//评分数据B:u1:18  u2:33   u3:22
			for (Text line : values) {
				String val = line.toString();
				if (val.startsWith("A:")) {// 表示item同现数字
					// A:i109,1
					String[] kv = Pattern.compile("[\t,]").split(
							val.substring(2));
					// b:2
					// c:4
					// d:8
					try {
						mapA.put(kv[0], Integer.parseInt(kv[1]));
										//item同现A:b:2  c:4   d:8
						//基于 A,item同现次数
					} catch (Exception e) {
						e.printStackTrace();
					}

				} else if (val.startsWith("B:")) {
					 // B:u401,2
					String[] kv = Pattern.compile("[\t,]").split(
							val.substring(2));
							//评分数据B:u1:18  u2:33   u3:22
					try {
						mapB.put(kv[0], Integer.parseInt(kv[1]));
					} catch (Exception e) {
						e.printStackTrace();
					}
				}
			}

			double result = 0;
			//同现
			// itemID

			for (String mapk : mapA.keySet()) {
				int num = mapA.get(mapk);  //对于A的同现次数


				//评分
				// userID
				for (String mapkb : mapB.keySet()) {
					int pref = mapB.get(mapkb);
					result = num * pref;// 矩阵乘法相乘计算，
					// 矩阵乘法本质上是第一列和第一行相乘，第二列和第二行相乘....然后把所有的对应值加起来

					Text k = new Text(mapkb);  //userID为key
					Text v = new Text(mapk + "," + result);//基于item,其他item的同现与评分(所有user对item)乘积
					context.write(k, v);
				}
			}
		}
	}
}
